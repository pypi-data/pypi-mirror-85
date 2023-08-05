#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Communication protocol implementing an OPC UA connection.
This protocol is used to interface with the "Supercube" PLC from Siemens.
"""

import errno
import logging
from collections.abc import Iterable as IterableBase
from concurrent.futures import CancelledError, TimeoutError
from functools import wraps
from logging import Logger
from socket import gaierror
from time import sleep
from typing import Iterable, Union, Optional

from opcua import Client, Node, Subscription
from opcua.ua import NodeId, DataValue, UaError
from opcua.ua.uaerrors import BadSubscriptionIdInvalid

from .base import CommunicationProtocol
from ..configuration import configdataclass


class OpcUaSubHandler:
    """
    Base class for subscription handling of OPC events and data change events.
    Override methods from this class to add own handling capabilities.

    To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing.
    """

    def datachange_notification(self, node, val, data):
        logging.getLogger(__name__).debug(
            f"OPCUA Datachange event: {node} to value {val}"
        )

    def event_notification(self, event):
        logging.getLogger(__name__).debug(f"OPCUA Event: {event}")


@configdataclass
class OpcUaCommunicationConfig:
    """
    Configuration dataclass for OPC UA Communciation.
    """

    #: Hostname or IP-Address of the OPC UA server.
    host: str

    #: Endpoint of the OPC server, this is a path like 'OPCUA/SimulationServer'
    endpoint_name: str

    #: Port of the OPC UA server to connect to.
    port: int = 4840

    #: object to use for handling subscriptions.
    sub_handler: OpcUaSubHandler = OpcUaSubHandler()

    #: Update period for generating datachange events in OPC UA [milli seconds]
    update_period: int = 500

    #: Wait time between re-trying calls on underlying OPC UA client timeout error
    wait_timeout_retry_sec: Union[int, float] = 1

    #: Maximal number of call re-tries on underlying OPC UA client timeout error
    max_timeout_retry_nr: int = 5

    def clean_values(self):
        if self.update_period <= 0:
            raise ValueError(
                "Update period for generating datachange events (msec) needs to be "
                "a positive integer."
            )
        if self.wait_timeout_retry_sec <= 0:
            raise ValueError(
                "Re-try wait time (sec) on timeout needs to be a positive number."
            )
        if self.max_timeout_retry_nr < 0:
            raise ValueError(
                "Maximal re-tries count on timeout needs to be non-negative integer."
            )


class OpcUaCommunicationIOError(IOError):
    """OPC-UA communication I/O error."""


class OpcUaCommunicationTimeoutError(OpcUaCommunicationIOError):
    """OPC-UA communication timeout error."""


def _log_error(
    log: Logger, e: Exception, msg_prefix: str = "", add_traceback: bool = False,
) -> None:
    """
    Log error message.

    :param log: logger to use
    :param e: error to log
    :param msg_prefix: error message prefix added before error class name and message
    :param add_traceback: if to append last error traceback to the log message
    """
    msg_suffix = ""
    if add_traceback:
        import traceback
        msg_suffix = f"\n{traceback.format_exc()}"
    log.error(f"{msg_prefix}{e.__class__.__name__}: {str(e)}{msg_suffix}")


#: current number of reopen tries on OPC UA connection error
_n_timeout_retry = 0


def _wrap_ua_error(method):
    """
    Wrap any `UaError` raised from a `OpcUaCommunication` method into
    `OpcUaCommunicationIOError`; additionally, log source error.

    :param method: `OpcUaCommunication` instance method to wrap
    :return: Whatever `method` returns
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        try:

            result = method(self, *args, **kwargs)

        except UaError as e:

            _log_error(self.logger, e, "OPC UA client runtime error: ", True)
            raise OpcUaCommunicationIOError from e

        except gaierror as e:

            _log_error(self.logger, e, "Socket address error: ", True)
            raise OpcUaCommunicationIOError from e

        except OSError as e:

            if e.errno == errno.EBADF:
                log_prefix = "OPC UA client socket error: "
            else:
                log_prefix = "OPC UA client OS error: "
            _log_error(self.logger, e, log_prefix, True)
            raise OpcUaCommunicationIOError from e

        except CancelledError as e:

            _log_error(self.logger, e, "OPC UA client thread cancelled error: ", True)
            raise OpcUaCommunicationIOError from e

        except TimeoutError as e:

            _log_error(self.logger, e, "OPC UA client thread timeout error: ", True)
            # try close, re-open and re-call
            global _n_timeout_retry
            _max_try_reopen = self.config.max_timeout_retry_nr
            if _n_timeout_retry < _max_try_reopen:
                sleep(self.config.wait_timeout_retry_sec)
                _n_timeout_retry += 1

                self.logger.info(
                    f"OPC UA client retry #{_n_timeout_retry}/#{_max_try_reopen}:"
                    f" {method}"
                )

                # note: nested re-tries use the global counter to stop on max limit
                result = wrapper(self, *args, **kwargs)
                # success => reset global counter
                _n_timeout_retry = 0

            else:
                # failure => reset global counter
                _n_timeout_retry = 0
                # raise from original timeout error
                raise OpcUaCommunicationTimeoutError from e

        return result

    return wrapper


def _require_ua_opened(method):
    """
    Check if `opcua.client.ua_client.UaClient` socket is opened and raise an
    `OpcUaCommunicationIOError` if not.

    NOTE: this checks should be implemented downstream in
    `opcua.client.ua_client.UaClient`; currently you get `AttributeError: 'NoneType'
    object has no attribute ...`.

    :param method: `OpcUaCommunication` instance method to wrap
    :return: Whatever `method` returns
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # BLAH: this checks should be implemented downstream in
        # `opcua.client.ua_client.UaClient`
        if self._client.uaclient._uasocket is None:
            err_msg = f"Client's socket is not set in {str(self)}. Was it opened?"
            self.logger.error(err_msg)
            raise OpcUaCommunicationIOError(err_msg)
        return method(self, *args, **kwargs)

    return wrapper


class OpcUaCommunication(CommunicationProtocol):
    """
    Communication protocol implementing an OPC UA connection.
    Makes use of the package python-opcua.
    """

    def __init__(self, config) -> None:
        """
        Constructor for OpcUaCommunication.

        :param config: is the configuration dictionary.
        """

        super().__init__(config)

        self.logger = logging.getLogger(__name__)

        conf = self.config
        url = f"opc.tcp://{conf.host}:{conf.port}/{conf.endpoint_name}"

        self.logger.info(f"Create OPC UA client to URL: {url}")

        self._client = Client(url)

        # the objects node exists on every OPC UA server and are root for all objects.
        self._objects_node: Optional[Node] = None

        # subscription handler
        self._sub_handler = self.config.sub_handler

        # subscription object
        self._subscription: Optional[Subscription] = None

    @staticmethod
    def config_cls():
        return OpcUaCommunicationConfig

    @_wrap_ua_error
    def open(self) -> None:
        """
        Open the communication to the OPC UA server.

        :raises OpcUaCommunicationIOError: when communication port cannot be opened.
        """

        self.logger.info("Open connection to OPC server.")
        with self.access_lock:
            self._client.connect()
            # in example from opcua, load_type_definitions() is called after connect(
            # ). However, this raises ValueError when connecting to Siemens S7,
            # and no problems are detected omitting this call.
            # self._client.load_type_definitions()
            self._objects_node = self._client.get_objects_node()
            self._subscription = self._client.create_subscription(
                self.config.update_period, self._sub_handler
            )

    @property
    def is_open(self) -> bool:
        """
        Flag indicating if the communication port is open.

        :return: `True` if the port is open, otherwise `False`
        """
        open_called = self._objects_node or self._subscription
        if open_called:
            try:
                self._client.send_hello()
                return True
            except UaError as e:
                self.logger.info(f"Sending hello returned UA error: {str(e)}")
                # try cleanup in case connection was opened before but now is lost
                if open_called:
                    self.close()
        return False

    @_wrap_ua_error
    def close(self) -> None:
        """
        Close the connection to the OPC UA server.
        """

        self.logger.info("Close connection to OPC server.")
        with self.access_lock:
            if self._subscription:
                try:
                    self._subscription.delete()
                except BadSubscriptionIdInvalid:
                    pass
                self._subscription = None
            if self._objects_node:
                self._objects_node = None
            self._client.disconnect()

    @_require_ua_opened
    @_wrap_ua_error
    def read(self, node_id, ns_index):
        """
        Read a value from a node with id and namespace index.

        :param node_id: the ID of the node to read the value from
        :param ns_index: the namespace index of the node
        :return: the value of the node object.
        :raises OpcUaCommunicationIOError: when protocol was not opened or can't
            communicate with a OPC UA server
        """

        with self.access_lock:
            return self._client.get_node(
                NodeId(identifier=node_id, namespaceidx=ns_index)
            ).get_value()

    @_require_ua_opened
    @_wrap_ua_error
    def write(self, node_id, ns_index, value) -> None:
        """
        Write a value to a node with name ``name``.

        :param node_id: the id of the node to write the value to.
        :param ns_index: the namespace index of the node.
        :param value: the value to write.
        :raises OpcUaCommunicationIOError: when protocol was not opened or can't
            communicate with a OPC UA server
        """

        with self.access_lock:
            self._client.get_node(
                NodeId(identifier=node_id, namespaceidx=ns_index)
            ).set_value(DataValue(value))

    @_require_ua_opened
    @_wrap_ua_error
    def init_monitored_nodes(
        self, node_id: Union[object, Iterable], ns_index: int
    ) -> None:
        """
        Initialize monitored nodes.

        :param node_id: one or more strings of node IDs; node IDs are always casted
            via `str()` method here, hence do not have to be strictly string objects.
        :param ns_index: the namespace index the nodes belong to.
        :raises OpcUaCommunicationIOError: when protocol was not opened or can't
            communicate with a OPC UA server
        """

        if not self._subscription:
            err_msg = f"Missing subscription in {str(self)}. Was it opened?"
            self.logger.error(err_msg)
            raise OpcUaCommunicationIOError(err_msg)

        ids: Iterable[object] = (
            node_id
            if not isinstance(node_id, str) and isinstance(node_id, IterableBase)
            else (node_id,)
        )

        nodes = []
        for id_ in ids:
            nodes.append(
                self._client.get_node(
                    NodeId(identifier=str(id_), namespaceidx=ns_index)
                )
            )

        with self.access_lock:
            self._subscription.subscribe_data_change(nodes)
