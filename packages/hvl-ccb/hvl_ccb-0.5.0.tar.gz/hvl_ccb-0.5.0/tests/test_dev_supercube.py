#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Test module for the Supercube base device class.
"""

import logging
from time import sleep
from typing import List

import pytest
from pytest_mock import MockerFixture

from hvl_ccb.comm import OpcUaCommunicationIOError, OpcUaCommunicationTimeoutError
from hvl_ccb.dev.supercube import constants
from hvl_ccb.dev.supercube.base import (
    SupercubeBase,
    SupercubeConfiguration,
    SupercubeEarthingStickOperationError,
    SupercubeOpcUaCommunication,
)
from tests.opctools import DemoServer


@pytest.fixture(scope="module")
def dev_config():
    return {
        "namespace_index": 3,
        "polling_delay_sec": 0.05,
        "polling_interval_sec": 0.01,
    }


@pytest.fixture(scope="module")
def com_config():
    return {
        "host": "localhost",
        "port": 14123,
        "endpoint_name": "",
        "update_period": 10,
        "wait_timeout_retry_sec": 0.01,
        "max_timeout_retry_nr": 3,
    }


@pytest.fixture(scope="function")
def demo_opcua_server(dev_config):
    opcua_server = DemoServer(dev_config["namespace_index"], "B", 14123)
    opcua_server.start()

    # add socket nodes
    for socket in constants.GeneralSockets:
        opcua_server.add_var(socket, False, True)

    # add support input and output nodes
    for support in constants.GeneralSupport:
        opcua_server.add_var(support, False, True)

    for i, alarm in enumerate(constants.Alarms):
        opcua_server.add_var(alarm, bool(i % 2), False)

    # add remote control vars
    opcua_server.add_var(constants.OpcControl.active, False, True)
    opcua_server.add_var(constants.OpcControl.live, False, True)

    yield opcua_server

    opcua_server.stop()


@pytest.fixture(scope="function")
def opened_supercube_com(
    com_config, dev_config, demo_opcua_server: DemoServer,
):
    opc_comm = SupercubeOpcUaCommunication(com_config)
    opc_comm.open()
    yield opc_comm
    opc_comm.close()


def _get_logged_messages(
    caplog, expected_logger_name: str, expected_level: int,
) -> List[str]:
    return [
        message
        for logger_name, level, message in caplog.record_tuples
        if logger_name == expected_logger_name and level == expected_level
    ]


def test_supercube_subscription_handler_datachange_safetystatus(
    opened_supercube_com: SupercubeOpcUaCommunication,
    dev_config: dict,
    demo_opcua_server: DemoServer,
    caplog,  # pytest._logging.LogCaptureFixture
):
    ns_index = dev_config["namespace_index"]

    caplog.set_level(logging.INFO)

    # test a status datachange
    demo_opcua_server.add_var(
        constants.Safety.status, int(constants.SafetyStatus.Initializing), True,
    )
    opened_supercube_com.init_monitored_nodes(str(constants.Safety.status), ns_index)
    sleep(0.05)

    demo_opcua_server.set_var(
        constants.Safety.status, int(constants.SafetyStatus.GreenNotReady),
    )
    sleep(0.05)

    # FIXME: does not work in gitlab CI
    # check presence of log messages in a correct order
    # assert [
    #     f"Safety: {str(constants.SafetyStatus.Initializing)}",
    #     f"Safety: {str(constants.SafetyStatus.GreenNotReady)}",
    # ] == _get_logged_messages(caplog, "hvl_ccb.dev.supercube.base", logging.INFO)


def test_supercube_subscription_handler_datachange_earthingstickstatus(
    opened_supercube_com: SupercubeOpcUaCommunication,
    dev_config: dict,
    demo_opcua_server: DemoServer,
    caplog,  # pytest._logging.LogCaptureFixture
):
    ns_index = dev_config["namespace_index"]

    caplog.set_level(logging.INFO)

    # test an earthing stick status datachange
    ess_tuple = constants.EarthingStick.statuses()
    for ess in ess_tuple:
        demo_opcua_server.add_var(
            ess, int(constants.EarthingStickStatus.inactive), True,
        )
    opened_supercube_com.init_monitored_nodes(ess_tuple, ns_index)
    sleep(0.05)

    for ess in ess_tuple:
        demo_opcua_server.set_var(ess, int(constants.EarthingStickStatus.closed))
    sleep(0.05)

    # FIXME: does not work in gitlab CI
    # check presence of log messages in a correct order
    # assert (
    #     [
    #         f"Earthing {ess.number}: {str(constants.EarthingStickStatus.inactive)}"
    #         for ess in ess_tuple
    #     ]
    #     + [
    #         f"Earthing {ess.number}: {str(constants.EarthingStickStatus.closed)}"
    #         for ess in ess_tuple
    #     ]
    # ) == _get_logged_messages(caplog, "hvl_ccb.dev.supercube.base", logging.INFO)


@pytest.fixture(scope="function")
def cube(com_config, dev_config, demo_opcua_server: DemoServer):
    cube = SupercubeBase(com_config, dev_config)
    cube.start()
    yield cube
    cube.stop()


def test_dev_config(dev_config):
    # currently there are no non-default config values
    SupercubeConfiguration()

    config = SupercubeConfiguration(**dev_config)
    for key, value in dev_config.items():
        assert getattr(config, key) == value


@pytest.mark.parametrize(
    "wrong_config_dict",
    [
        {"namespace_index": -1},
        {"polling_interval_sec": -1},
        {"polling_interval_sec": 0},
        {"polling_delay_sec": -1},
    ],
)
def test_invalid_config_dict(dev_config, wrong_config_dict):
    invalid_config = dict(dev_config)
    invalid_config.update(wrong_config_dict)
    with pytest.raises(ValueError):
        SupercubeConfiguration(**invalid_config)


def test_set_remote_control(cube: SupercubeBase, demo_opcua_server: DemoServer):
    cube.set_remote_control(False)
    assert demo_opcua_server.get_var(constants.OpcControl.active) is False
    cube.set_remote_control(True)
    assert demo_opcua_server.get_var(constants.OpcControl.active) is True


def test_status_poller(
    com_config, dev_config, demo_opcua_server: DemoServer, mocker: MockerFixture,
):

    cube = SupercubeBase(com_config, dev_config)
    poller = cube.status_poller
    assert poller is not None
    assert poller.polling_delay_sec == dev_config["polling_delay_sec"]
    assert poller.polling_interval_sec == dev_config["polling_interval_sec"]
    assert poller.polling_timeout_sec is None
    assert poller.spoll_handler == cube._spoll_handler

    spy_spoll_handler = mocker.spy(poller, "spoll_handler")
    spy_start_polling = mocker.spy(poller, "start_polling")
    spy_stop_polling = mocker.spy(poller, "stop_polling")

    poller.stop_polling()
    assert spy_stop_polling.spy_return is False

    cube.start()

    spy_start_polling.assert_called()
    assert spy_start_polling.spy_return is True

    poller.start_polling()
    assert spy_start_polling.spy_return is False

    sleep(dev_config["polling_delay_sec"] + 3 * dev_config["polling_interval_sec"])
    spy_spoll_handler.assert_called()
    assert spy_spoll_handler.spy_return is None

    cube.stop()
    spy_stop_polling.assert_called()
    assert spy_stop_polling.spy_return is True


def test_status_poller_timeout_error(
    com_config, dev_config, demo_opcua_server: DemoServer, mocker: MockerFixture,
):

    cube = SupercubeBase(com_config, dev_config)
    cube.start()
    assert cube.status_poller.is_polling()
    assert cube.com.is_open

    # patch UASocketClient.send_request to raise a mock TimeoutError as if coming from
    # used therein concurrent.futures.Future;
    # raise error only on disable remote control done via poller thread on stop()
    # => write(constants.OpcControl.active, False)

    # Use bound method (otherwise live unpatch does not work):
    send_request_orig = cube.com._client.uaclient._uasocket.send_request

    def send_request(self, request, *args, **kwargs):
        if (
            hasattr(request, "Parameters")
            and hasattr(request.Parameters, "NodesToWrite")
        ):
            node_to_write = request.Parameters.NodesToWrite[0]
            if (
                node_to_write.NodeId.Identifier == constants.OpcControl.active
                and node_to_write.Value.Value.Value is False
            ):
                from concurrent.futures import TimeoutError

                raise TimeoutError("mock timeout error")
        # method already bound - ignore `self`
        return send_request_orig(request, *args, **kwargs)

    mocker.patch(
        "opcua.client.ua_client.UASocketClient.send_request",
        side_effect=send_request,
        autospec=True,
    )

    # check poller thread error caught and wrapped
    with pytest.raises(OpcUaCommunicationTimeoutError):
        cube.set_remote_control(False)
    assert not cube.status_poller.is_polling()
    assert cube.com.is_open

    # check that stopping also does raises the error, but cleans up otherwise
    with pytest.raises(OpcUaCommunicationTimeoutError):
        cube.stop()
    assert not cube.status_poller.is_polling()
    assert not cube.com.is_open

    # unpatch and try to stop dev again - will raise error due to broken com,
    # but not the timeout
    mocker.patch(
        "opcua.client.ua_client.UASocketClient.send_request",
        side_effect=send_request_orig,
    )

    with pytest.raises(OpcUaCommunicationIOError) as excinfo:
        cube.stop()
        assert excinfo.type is not OpcUaCommunicationTimeoutError
    assert not cube.status_poller.is_polling()
    assert not cube.com.is_open


def test_get_support_input(cube: SupercubeBase):
    assert cube.get_support_input(1, 1) is False

    with pytest.raises(ValueError):
        cube.get_support_input(1, 123)
    with pytest.raises(ValueError):
        cube.get_support_input(123, 1)


def test_get_set_support_output(cube: SupercubeBase):
    cube.set_support_output(1, 1, False)
    assert cube.get_support_output(1, 1) is False
    cube.set_support_output(1, 1, True)
    assert cube.get_support_output(1, 1) is True

    with pytest.raises(ValueError):
        cube.get_support_output(1, 123)
    with pytest.raises(ValueError):
        cube.get_support_output(123, 1)
    with pytest.raises(ValueError):
        cube.set_support_output(1, 123, False)
    with pytest.raises(ValueError):
        cube.set_support_output(123, 1, False)


def test_set_support_output_impulse(cube: SupercubeBase):
    cube.set_support_output_impulse(2, 2, 0.01, True)

    with pytest.raises(ValueError):
        cube.set_support_output_impulse(1, 123)
    with pytest.raises(ValueError):
        cube.set_support_output_impulse(123, 1)


def test_get_t13_socket(cube: SupercubeBase):
    assert cube.get_t13_socket(1) is False
    cube.set_t13_socket(1, True)
    assert cube.get_t13_socket(1) is True

    with pytest.raises(ValueError):
        cube.get_t13_socket(4)


def test_set_t13_socket(cube: SupercubeBase):
    cube.set_t13_socket(1, True)

    with pytest.raises(ValueError):
        cube.set_t13_socket(4, False)

    with pytest.raises(ValueError):
        cube.set_t13_socket(1, "on")


def test_get_cee16(cube: SupercubeBase):
    cube.set_cee16_socket(False)
    assert cube.get_cee16_socket() is False
    cube.set_cee16_socket(True)
    assert cube.get_cee16_socket() is True


def test_set_cee16(cube: SupercubeBase):
    cube.set_cee16_socket(True)
    cube.set_cee16_socket(False)

    with pytest.raises(ValueError):
        cube.set_cee16_socket(1)

    with pytest.raises(ValueError):
        cube.set_cee16_socket("on")


def test_get_status(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.Safety.status, 1, False)
    assert cube.get_status() == constants.SafetyStatus.GreenNotReady

    demo_opcua_server.set_var(constants.Safety.status, 2)
    assert cube.get_status() == constants.SafetyStatus.GreenReady


def test_ready(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.Safety.switch_to_ready, False, True)
    cube.ready(True)
    assert demo_opcua_server.get_var(constants.Safety.switch_to_ready) is True


def test_operate(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.Safety.switch_to_operate, False, True)
    cube.operate(True)
    assert demo_opcua_server.get_var(constants.Safety.switch_to_operate) is True


def test_get_measurement_ratio(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.MeasurementsDividerRatio.input_1, 123.4, False)
    assert cube.get_measurement_ratio(1) == 123.4

    with pytest.raises(ValueError):
        cube.get_measurement_ratio(123)


def test_get_measurement_voltage(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.MeasurementsScaledInput.input_1, 110_000, False)
    assert cube.get_measurement_voltage(1) == 110_000.0

    with pytest.raises(ValueError):
        cube.get_measurement_voltage(123)


def test_get_earthing_stick_status(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.EarthingStick.status_1, 1, False)
    assert cube.get_earthing_stick_status(1) == constants.EarthingStickStatus(1)

    with pytest.raises(ValueError):
        cube.get_earthing_stick_status(123)


def test_get_earthing_stick_operating_status(
    cube: SupercubeBase, demo_opcua_server: DemoServer
):
    demo_opcua_server.add_var(
        constants.EarthingStick.operating_status_1,
        constants.EarthingStickOperatingStatus.auto,
        False,
    )
    assert (
        cube.get_earthing_stick_operating_status(1)
        is constants.EarthingStickOperatingStatus.auto
    )

    with pytest.raises(ValueError):
        cube.get_earthing_stick_operating_status(123)


def test_get_earthing_stick_manual(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(
        constants.EarthingStick.manual_1,
        bool(constants.EarthingStickOperation.close),
        False,
    )
    assert cube.get_earthing_stick_manual(1) is constants.EarthingStickOperation.close

    with pytest.raises(ValueError):
        cube.get_earthing_stick_manual(123)


def test_operate_earthing_stick(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(
        constants.EarthingStick.operating_status_1,
        constants.EarthingStickOperatingStatus.manual,
        False,
    )
    demo_opcua_server.add_var(
        constants.EarthingStick.manual_1,
        bool(constants.EarthingStickOperation.open),
        True,
    )
    assert cube.get_earthing_stick_manual(1) is constants.EarthingStickOperation.open
    cube.operate_earthing_stick(1, constants.EarthingStickOperation.close)
    assert cube.get_earthing_stick_manual(1) is constants.EarthingStickOperation.close


def test_operate_earthing_stick_error(
    cube: SupercubeBase, demo_opcua_server: DemoServer,
):
    demo_opcua_server.add_var(
        constants.EarthingStick.operating_status_1,
        constants.EarthingStickOperatingStatus.auto,
        False,
    )
    with pytest.raises(SupercubeEarthingStickOperationError):
        cube.operate_earthing_stick(1, constants.EarthingStickOperation.close)


def test_quit_error(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.Errors.quit, False, True)
    cube.quit_error()
    assert demo_opcua_server.get_var(constants.Errors.quit) is False


def test_get_door_status(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.Door.status_1, 2, False)
    assert cube.get_door_status(1) == constants.DoorStatus(2)


def test_get_earthing_rod_status(cube: SupercubeBase, demo_opcua_server: DemoServer):
    demo_opcua_server.add_var(constants.EarthingRod.status_1, 0, False)
    assert cube.get_earthing_rod_status(1) == constants.EarthingRodStatus(0)


def test_set_status_board(cube: SupercubeBase, demo_opcua_server: DemoServer):

    n_max = len(constants.MessageBoard)

    with pytest.raises(ValueError):
        cube.set_status_board(["x"] * (n_max + 1))
    with pytest.raises(ValueError):
        cube.set_status_board(["x"], pos=[n_max])

    for line in constants.MessageBoard:
        demo_opcua_server.add_var(line, "", True)

    msgs = ["Hello World", "Hello Fabian", "Hello HVL"]

    cube.set_status_board(msgs[:1])
    assert demo_opcua_server.get_var(constants.MessageBoard.line(1)) == msgs[0]
    cube.set_status_board(msgs[:1], pos=[1], clear_board=False)
    assert demo_opcua_server.get_var(constants.MessageBoard.line(1)) == msgs[0]
    assert demo_opcua_server.get_var(constants.MessageBoard.line(2)) == msgs[0]

    positions = [4, 8, 12]
    cube.set_status_board(msgs, positions, clear_board=False)
    for i, p in enumerate(positions):
        assert demo_opcua_server.get_var(constants.MessageBoard.line(p+1)) == msgs[i]

    cube.set_status_board([str(i) for i in range(15)])
    for i in range(15):
        assert demo_opcua_server.get_var(constants.MessageBoard.line(i+1)) == str(i)


def test_set_message_board(cube: SupercubeBase, demo_opcua_server: DemoServer):

    n_max = len(constants.MessageBoard)

    with pytest.raises(ValueError):
        cube.set_message_board(["x"] * (n_max + 1))

    for line in constants.MessageBoard:
        demo_opcua_server.add_var(line, "", True)

    msgs = ["ERROR: This is unexpected", "Good choice"]
    cube.set_message_board(msgs[:1])
    assert demo_opcua_server.get_var(constants.MessageBoard.line(1)).endswith(msgs[0])

    # push two messages to first two lines, in the given order
    cube.set_message_board(msgs)
    assert demo_opcua_server.get_var(constants.MessageBoard.line(1)).endswith(msgs[0])
    assert demo_opcua_server.get_var(constants.MessageBoard.line(2)).endswith(msgs[1])
    assert demo_opcua_server.get_var(constants.MessageBoard.line(3)).endswith(msgs[0])

    # overwrite all messages except last, which is pushed to be last line
    cube.set_message_board("x" * (n_max - 1))
    for n in range(len(constants.MessageBoard)-1):
        assert demo_opcua_server.get_var(constants.MessageBoard.line(n+1)).endswith("x")
    last_msg = demo_opcua_server.get_var(constants.MessageBoard.line(n_max))
    assert last_msg.endswith(msgs[0])
