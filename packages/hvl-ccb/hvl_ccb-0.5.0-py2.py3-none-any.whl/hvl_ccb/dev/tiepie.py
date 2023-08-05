#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
This module is a wrapper around libtiepie Oscilloscope devices; see
https://www.tiepie.com/en/libtiepie-sdk .

The device classes adds simplifications for starting of the device (using serial
number) and managing mutable configuration of both the device and oscilloscope's
channels. This includes extra validation and typing hints support.

To install libtiepie:

1. download libtiepie

    For Windows download the library from
    https://www.tiepie.com/en/libtiepie-sdk/windows. If using the virtualenv copy the
    dynamic library file  `libtiepie.dll` into your project folder under
    `.venv/Scripts/`, where `.venv/` is your virtual environment folder.

2. install the Python bindings

    $ pip install python-libtiepie

"""
from __future__ import annotations

import array
import logging
import time
from collections import Sequence
from functools import wraps
from typing import (
    cast,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from aenum import IntEnum

try:
    import numpy as np  # type: ignore
except ImportError:
    from collections import namedtuple

    _npt = namedtuple("np", "ndarray")
    np = _npt(ndarray=type(None))
    _has_numpy = False
else:
    _has_numpy = True

import libtiepie as ltp
from libtiepie.exceptions import LibTiePieException, InvalidDeviceSerialNumberError
from libtiepie import oscilloscope as ltp_osc
from libtiepie import generator as ltp_gen
from libtiepie import oscilloscopechannel as ltp_osc_ch
from libtiepie import i2chost as ltp_i2c

from .base import SingleCommDevice
from ..comm import NullCommunicationProtocol
from ..configuration import configdataclass
from ..utils.enum import NameEnum
from ..utils.typing import Number


@configdataclass
class TiePieDeviceConfig:
    """
    Configuration dataclass for TiePie
    """

    serial_number: int
    require_block_measurement_support: bool = True
    n_max_try_get_device: int = 10
    wait_sec_retry_get_device: Number = 1.0

    def clean_values(self):
        if self.serial_number <= 0:
            raise ValueError("serial_number must be a positive integer.")
        if self.n_max_try_get_device <= 0:
            raise ValueError("n_max_try_get_device must be an positive integer.")
        if self.wait_sec_retry_get_device <= 0:
            raise ValueError("wait_sec_retry_get_device must be a positive number.")


class TiePieDeviceType(NameEnum):
    """
    TiePie device type.
    """

    _init_ = "value ltp_class"
    OSCILLOSCOPE = ltp.DEVICETYPE_OSCILLOSCOPE, ltp_osc.Oscilloscope
    I2C = ltp.DEVICETYPE_I2CHOST, ltp_i2c.I2CHost
    GENERATOR = ltp.DEVICETYPE_GENERATOR, ltp_gen.Generator


class TiePieOscilloscopeTriggerLevelMode(NameEnum):
    _init_ = "value description"
    UNKNOWN = ltp.TLM_UNKNOWN, "Unknown"
    RELATIVE = ltp.TLM_RELATIVE, "Relative"
    ABSOLUTE = ltp.TLM_ABSOLUTE, "Absolute"


class TiePieOscilloscopeChannelCoupling(NameEnum):
    _init_ = "value description"
    DCV = ltp.CK_DCV, "DC volt"
    ACV = ltp.CK_ACV, "AC volt"
    DCA = ltp.CK_DCA, "DC current"
    ACA = ltp.CK_ACA, "AC current"


class TiePieOscilloscopeTriggerKind(NameEnum):
    _init_ = "value description"
    RISING = ltp.TK_RISINGEDGE, "Rising"
    FALLING = ltp.TK_FALLINGEDGE, "Falling"
    ANY = ltp.TK_ANYEDGE, "Any"
    RISING_OR_FALLING = ltp.TK_ANYEDGE, "Rising or Falling"


class TiePieOscilloscopeRange(NameEnum):
    TWO_HUNDRED_MILLI_VOLT = 0.2
    FOUR_HUNDRED_MILLI_VOLT = 0.4
    EIGHT_HUNDRED_MILLI_VOLT = 0.8
    TWO_VOLT = 2
    FOUR_VOLT = 4
    EIGHT_VOLT = 8
    TWENTY_VOLT = 20
    FORTY_VOLT = 40
    EIGHTY_VOLT = 80

    @staticmethod
    def suitable_range(value):
        try:
            return TiePieOscilloscopeRange(value)
        except ValueError:
            attrs = [ra.value for ra in TiePieOscilloscopeRange]
            chosen_range: Optional[TiePieOscilloscopeRange] = None
            for attr in attrs:
                if value < attr:
                    chosen_range = TiePieOscilloscopeRange(attr)
                    logging.warning(
                        f"Desired value ({value} V) not possible."
                        f"Next larger range ({chosen_range.value} V) "
                        f"selected."
                    )
                    break
            if chosen_range is None:
                chosen_range = TiePieOscilloscopeRange.EIGHTY_VOLT
                logging.warning(
                    f"Desired value ({value} V) is over the maximum; "
                    f"largest range ({chosen_range.value} V) selected"
                )
            return chosen_range


class TiePieOscilloscopeResolution(IntEnum):
    EIGHT_BIT = 8
    TWELVE_BIT = 12
    FOURTEEN_BIT = 14
    SIXTEEN_BIT = 16


class TiePieGeneratorSignalType(NameEnum):
    _init_ = "value description"
    UNKNOWN = ltp.ST_UNKNOWN, "Unknown"
    SINE = ltp.ST_SINE, "Sine"
    TRIANGLE = ltp.ST_TRIANGLE, "Triangle"
    SQUARE = ltp.ST_SQUARE, "Square"
    DC = ltp.ST_DC, "DC"
    NOISE = ltp.ST_NOISE, "Noise"
    ARBITRARY = ltp.ST_ARBITRARY, "Arbitrary"
    PULSE = ltp.ST_PULSE, "Pulse"


class TiePieOscilloscopeAutoResolutionModes(NameEnum):
    _init_ = "value description"
    UNKNOWN = ltp.AR_UNKNOWN, "Unknown"
    DISABLED = ltp.AR_DISABLED, "Disabled"
    NATIVEONLY = ltp.AR_NATIVEONLY, "Native only"
    ALL = ltp.AR_ALL, "All"


class TiePieError(Exception):
    """
    Error of the class TiePie
    """

    pass


def wrap_libtiepie_exception(func: Callable) -> Callable:
    """
    Decorator wrapper for `libtiepie` methods that use
    `libtiepie.library.check_last_status_raise_on_error()` calls.

    :param func: Function or method to be wrapped
    :raises TiePieError: instead of `LibTiePieException` or one of its subtypes.
    :return: whatever `func` returns
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LibTiePieException as e:
            logging.error(str(e))
            raise TiePieError from e

    return wrapped_func


_LtpDeviceReturnType = TypeVar('_LtpDeviceReturnType')
"""
An auxiliary typing hint of a `libtiepie` device type for return value of
the `get_device_by_serial_number` function and the wrapper methods using it.
"""


@wrap_libtiepie_exception
def get_device_by_serial_number(
    serial_number: int,
    # Note: TiePieDeviceType aenum as a tuple to define a return value type
    device_type: Union[str, Tuple[int, _LtpDeviceReturnType]],
    n_max_try_get_device: int = 10,
    wait_sec_retry_get_device: float = 1.0,
) -> _LtpDeviceReturnType:
    """
    Open and return handle of TiePie device with a given serial number

    :param serial_number: int serial number of the device
    :param device_type: a `TiePieDeviceType` instance containing device identifier (int
        number) and its corresponding class, both from `libtiepie`, or a string name
        of such instance
    :param n_max_try_get_device: maximal number of device list updates (int number)
    :param wait_sec_retry_get_device: waiting time in seconds between retries (int
        number)
    :return: Instance of a `libtiepie`  device class according to the specified
        `device_type`
    :raises TiePieError: when there is no device with given serial number
    :raises ValueError: when `device_type` is not an instance of `TiePieDeviceType`
    """

    device_type = TiePieDeviceType(device_type)

    # include network search with ltp.device_list.update()
    ltp.network.auto_detect_enabled = True

    n_try = 0
    device_list_item: Optional[ltp.devicelistitem.DeviceListItem] = None
    while device_list_item is None and n_try < n_max_try_get_device:
        n_try += 1
        ltp.device_list.update()
        if not ltp.device_list:
            msg = f"Searching for device... (attempt #{n_try}/{n_max_try_get_device})"
            if n_try < n_max_try_get_device:
                logging.warning(msg)
                time.sleep(wait_sec_retry_get_device)
                continue
            msg = f"No devices found to start (attempt #{n_try}/{n_max_try_get_device})"
            logging.error(msg)
            raise TiePieError(msg)

        # if a device is found
        try:
            device_list_item = ltp.device_list.get_item_by_serial_number(serial_number)
        except InvalidDeviceSerialNumberError as e:
            msg = (
                f"The device with serial number {serial_number} is not "
                f"available; attempt #{n_try}/{n_max_try_get_device}."
            )
            if n_try < n_max_try_get_device:
                logging.warning(msg)
                time.sleep(wait_sec_retry_get_device)
                continue
            logging.error(msg)
            raise TiePieError from e
    assert device_list_item is not None

    if not device_list_item.can_open(device_type.value):
        msg = (
            f"The device with serial number {serial_number} has no "
            f"{device_type} available."
        )
        logging.error(msg)
        raise TiePieError(msg)

    return device_list_item.open_device(device_type.value)


def _verify_via_libtiepie(
    dev_obj: ltp.device.Device, verify_method_suffix: str, value: float
) -> float:
    """
    Generic wrapper for `verify_SOMETHING` methods of the `libtiepie` device.
    Additionally to returning a value that will be actually set,
    gives an warning.

    :param dev_obj: TiePie device object, which has the verify_SOMETHING method
    :param verify_method_suffix: `libtiepie` devices verify_SOMETHING method
    :param value: numeric value
    :returns: Value that will be actually set instead of `value`.
    :raises TiePieError: when status of underlying device gives an error
    """
    verify_method = getattr(
        dev_obj,
        f"verify_{verify_method_suffix}",
    )
    will_have_value = verify_method(value)
    if will_have_value != value:
        msg = (
            f"Can't set {verify_method_suffix} to "
            f"{value}; instead {will_have_value} will be set."
        )
        logging.warning(msg)
    return will_have_value


def log_set(prop_name: str, prop_value: object, value_suffix: str = "") -> None:
    logging.info(f"{prop_name} is set to {prop_value}{value_suffix}.")


def _validate_number(
    x_name: str,
    x: object,
    limits: Tuple = (None, None),
    number_type: Union[Type[Number], Tuple[Type[Number], ...]] = (int, float),
) -> None:
    """
    Validate if given input `x` is a number of given `number_type` type, with value
    between given `limits[0]` and `limits[1]` (inclusive), if not `None`.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as number of given type within given range
    :param limits: [lower, upper] limit, with `None` denoting no limit: [-inf, +inf]
    :param number_type: expected type of a number, by default `float`
    :raises TypeError: when the validated input does not have expected type
    :raises ValueError: when the validated input has correct number type but is not
        within given range
    """
    if limits is None:
        limits = (None, None)
    msg = None
    err_cls: Optional[Type[Exception]] = None
    if not isinstance(number_type, Sequence):
        number_type = (number_type,)
    if not isinstance(x, number_type):
        msg = (
            f"{x_name} = {x} has to be of type "
            f"{' or '.join(nt.__name__ for nt in number_type)}"
        )
        err_cls = TypeError
    elif not (
        (limits[0] is None or cast(Number, x) >= limits[0])
        and (limits[1] is None or cast(Number, x) <= limits[1])
    ):
        if limits[0] is None:
            suffix = f"less or equal than {limits[1]}"
        elif limits[1] is None:
            suffix = f"greater or equal than {limits[0]}"
        else:
            suffix = f"between {limits[0]} and {limits[1]} inclusive"
        msg = f"{x_name} = {x} has to be " + suffix
        err_cls = ValueError
    if err_cls is not None:
        logging.error(msg)
        raise err_cls(msg)


def _validate_bool(x_name: str, x: object) -> None:
    """
    Validate if given input `x` is a `bool`.

    :param x_name: string name of the validate input, use for the error message
    :param x: an input object to validate as boolean
    :raises TypeError: when the validated input does not have boolean type
    """
    if not isinstance(x, bool):
        msg = f"{x_name} = {x} has to of type bool"
        logging.error(msg)
        raise TypeError(msg)


class OscilloscopeParameterLimits:
    """
    Default limits for oscilloscope parameters.
    """

    def __init__(self, dev_osc: ltp_osc.Oscilloscope) -> None:
        self.record_length = (0, dev_osc.record_length_max)
        self.sample_frequency = (0, dev_osc.sample_frequency_max)  # [samples/s]
        self.pre_sample_ratio = (0, 1)
        self.trigger_delay = (0, dev_osc.trigger_delay_max)


class OscilloscopeChannelParameterLimits:
    """
    Default limits for oscilloscope channel parameters.
    """

    def __init__(self, osc_channel: ltp_osc_ch.OscilloscopeChannel) -> None:
        self.input_range = (0, 80)  # [V]
        self.probe_offset = (-1e6, 1e6)  # [V], [A] or [Ohm]
        self.trigger_hysteresis = (0, 1)
        self.trigger_level_rel = (0, 1)
        self.trigger_level_abs = (None, None)


class GeneratorParameterLimits:
    """
    Default limits for generator parameters.
    """

    def __init__(self, dev_gen: ltp_gen.Generator) -> None:
        self.frequency = (0, dev_gen.frequency_max)
        self.amplitude = (0, dev_gen.amplitude_max)
        self.offset = (None, dev_gen.offset_max)


class I2CHostParameterLimits:
    """
    Default limits for I2C host parameters.
    """

    def __init__(self, dev_i2c: ltp_i2c.I2CHost) -> None:
        # I2C Host
        pass


class PublicPropertiesReprMixin:
    """General purpose utility mixin that overwrites object representation to a one
    analogous to `dataclass` instances, but using public properties and their values
    instead of `fields`.
    """

    def _public_properties_gen(self):
        """
        Generator that returns instance's properties names and their values,
        for properties that do not start with `"_"`

        :return: attribute name and value tuples
        """
        for name in dir(self):
            if (
                not name.startswith("_")
                and hasattr(self.__class__, name)
                and isinstance(getattr(self.__class__, name), property)
            ):
                yield name, getattr(self, name)

    def __repr__(self):
        attrs = ", ".join([
            f"{name}={value!r}" for name, value in self._public_properties_gen()
        ])
        return f"{self.__class__.__qualname__ }({attrs})"


class TiePieOscilloscopeConfig(PublicPropertiesReprMixin):
    """
    Oscilloscope's configuration with cleaning of values in properties setters.
    """

    def __init__(self, dev_osc: ltp_osc.Oscilloscope):
        self.dev_osc: ltp_osc.Oscilloscope = dev_osc
        self.param_lim: OscilloscopeParameterLimits = OscilloscopeParameterLimits(
            dev_osc=dev_osc
        )

    def clean_pre_sample_ratio(self, pre_sample_ratio: float) -> float:
        _validate_number(
            "pre sample ratio", pre_sample_ratio, self.param_lim.pre_sample_ratio
        )
        return float(pre_sample_ratio)

    @property
    def pre_sample_ratio(self) -> float:
        return self.dev_osc.pre_sample_ratio

    @pre_sample_ratio.setter
    def pre_sample_ratio(self, pre_sample_ratio: float) -> None:
        """
        Set pre sample ratio

        :param pre_sample_ratio: pre sample ratio numeric value.
        :raise ValueError: If `pre_sample_ratio` is not a number between 0 and 1
            (inclusive).
        """
        self.dev_osc.pre_sample_ratio = self.clean_pre_sample_ratio(pre_sample_ratio)
        log_set("Pre-sample ratio", pre_sample_ratio)

    def clean_record_length(self, record_length: int) -> int:
        _validate_number(
            "record length",
            record_length,
            limits=self.param_lim.record_length,
            number_type=int,
        )
        record_length = int(
            _verify_via_libtiepie(self.dev_osc, "record_length", record_length)
        )
        return record_length

    @property
    def record_length(self) -> int:
        return self.dev_osc.record_length

    @record_length.setter
    def record_length(self, record_length: int) -> None:
        record_length = self.clean_record_length(record_length)
        self.dev_osc.record_length = record_length
        log_set("Record length", record_length, value_suffix=" sample")

    @staticmethod
    def clean_resolution(
        resolution: Union[int, TiePieOscilloscopeResolution]
    ) -> TiePieOscilloscopeResolution:
        if not isinstance(resolution, TiePieOscilloscopeRange):
            _validate_number("resolution", resolution, number_type=int)
        return TiePieOscilloscopeResolution(resolution)

    @property
    def resolution(self) -> TiePieOscilloscopeResolution:
        return self.dev_osc.resolution

    @resolution.setter
    def resolution(self, resolution: Union[int, TiePieOscilloscopeResolution]) -> None:
        """
        Setter for resolution of the Oscilloscope.

        :param resolution: resolution integer.
        :raises ValueError: if resolution is not one of
            `TiePieOscilloscopeResolution` instance or integer values
        """
        self.dev_osc.resolution = self.clean_resolution(resolution)
        log_set("Resolution", self.dev_osc.resolution, value_suffix=" bit")

    @staticmethod
    def clean_auto_resolution_mode(
        auto_resolution_mode: Union[int, TiePieOscilloscopeAutoResolutionModes]
    ) -> TiePieOscilloscopeAutoResolutionModes:
        if not isinstance(auto_resolution_mode, TiePieOscilloscopeAutoResolutionModes):
            _validate_number(
                "auto resolution mode", auto_resolution_mode, number_type=int
            )
        if isinstance(auto_resolution_mode, bool):
            msg = "Auto resolution mode cannot be of boolean type"
            logging.error(msg)
            raise TypeError
        return TiePieOscilloscopeAutoResolutionModes(auto_resolution_mode)

    @property
    def auto_resolution_mode(self) -> TiePieOscilloscopeAutoResolutionModes:
        return TiePieOscilloscopeAutoResolutionModes(self.dev_osc.auto_resolution_mode)

    @auto_resolution_mode.setter
    def auto_resolution_mode(self, auto_resolution_mode):
        self.dev_osc.auto_resolution_mode = self.clean_auto_resolution_mode(
            auto_resolution_mode
        ).value
        log_set("Auto resolution mode", auto_resolution_mode)

    def clean_sample_frequency(self, sample_frequency: float) -> float:
        _validate_number(
            "sample frequency", sample_frequency, self.param_lim.sample_frequency
        )
        sample_frequency = _verify_via_libtiepie(
            self.dev_osc, "sample_frequency", sample_frequency
        )
        return float(sample_frequency)

    @property
    def sample_frequency(self) -> float:
        return self.dev_osc.sample_frequency

    @sample_frequency.setter
    def sample_frequency(self, sample_frequency: float):
        """
        Set sample frequency of the oscilloscope.

        :param sample_frequency: frequency number to set
        :raises ValueError: when frequency is not in device range
        """
        sample_frequency = self.clean_sample_frequency(sample_frequency)
        self.dev_osc.sample_frequency = sample_frequency
        log_set("Sample frequency", f"{sample_frequency:.2e}", value_suffix=" sample/s")

    def clean_trigger_time_out(self, trigger_time_out: float) -> float:
        _validate_number("trigger time-out", trigger_time_out, limits=(0, None))
        trigger_time_out = _verify_via_libtiepie(
            self.dev_osc, "trigger_time_out", trigger_time_out
        )
        return float(trigger_time_out)

    @property
    def trigger_time_out(self) -> float:
        return self.dev_osc.trigger_time_out

    @trigger_time_out.setter
    def trigger_time_out(self, trigger_time_out: float) -> None:
        """
        Set trigger time-out.

        :param trigger_time_out: Trigger time-out value, in seconds; `0`  forces
            trigger to start immediately after starting a measurement.
        :raise ValueError: If trigger time-out is not a non-negative real number.
        """
        trigger_time_out = self.clean_trigger_time_out(trigger_time_out)
        self.dev_osc.trigger_time_out = trigger_time_out
        log_set("Trigger time-out", trigger_time_out, value_suffix=" s")


class TiePieGeneratorConfig(PublicPropertiesReprMixin):
    """
    Generator's configuration with cleaning of values in properties setters.
    """

    def __init__(self, dev_gen: ltp_gen.Generator):
        self.dev_gen: ltp_gen.Generator = dev_gen
        self.param_lim: GeneratorParameterLimits = GeneratorParameterLimits(
            dev_gen=dev_gen
        )

    def clean_frequency(self, frequency: float) -> float:
        _validate_number("Frequency", frequency, limits=self.param_lim.frequency)
        frequency = _verify_via_libtiepie(self.dev_gen, "frequency", frequency)
        return float(frequency)

    @property
    def frequency(self) -> float:
        return self.dev_gen.frequency

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        frequency = self.clean_frequency(frequency)
        self.dev_gen.frequency = frequency
        log_set("Generator frequency", frequency, value_suffix=" Hz")

    def clean_amplitude(self, amplitude: float) -> float:
        _validate_number(
            "Generator amplitude", amplitude, limits=self.param_lim.amplitude
        )
        amplitude = _verify_via_libtiepie(self.dev_gen, "amplitude", amplitude)
        return float(amplitude)

    @property
    def amplitude(self) -> float:
        return self.dev_gen.amplitude

    @amplitude.setter
    def amplitude(self, amplitude: float) -> None:
        amplitude = self.clean_amplitude(amplitude)
        self.dev_gen.amplitude = amplitude
        log_set("Generator amplitude", amplitude, value_suffix=" V")

    def clean_offset(self, offset: float) -> float:
        _validate_number("Generator offset", offset, limits=self.param_lim.offset)
        offset = _verify_via_libtiepie(self.dev_gen, "offset", offset)
        return float(offset)

    @property
    def offset(self) -> float:
        return self.dev_gen.offset

    @offset.setter
    def offset(self, offset: float) -> None:
        offset = self.clean_offset(offset)
        self.dev_gen.offset = offset
        log_set("Generator offset", offset, value_suffix=" V")

    @staticmethod
    def clean_signal_type(
        signal_type: Union[int, TiePieGeneratorSignalType]
    ) -> TiePieGeneratorSignalType:
        return TiePieGeneratorSignalType(signal_type)

    @property
    def signal_type(self) -> TiePieGeneratorSignalType:
        return TiePieGeneratorSignalType(self.dev_gen.signal_type)

    @signal_type.setter
    def signal_type(self, signal_type: Union[int, TiePieGeneratorSignalType]) -> None:
        self.dev_gen.signal_type = self.clean_signal_type(signal_type).value
        log_set("Signal type", signal_type)

    @staticmethod
    def clean_enabled(enabled: bool) -> bool:
        _validate_bool("channel enabled", enabled)
        return enabled

    @property
    def enabled(self) -> bool:
        return self.dev_gen.enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self.dev_gen.enabled = self.clean_enabled(enabled)
        if enabled:
            msg = "enabled"
        else:
            msg = "disabled"
        log_set("Generator", msg)


class TiePieI2CHostConfig(PublicPropertiesReprMixin):
    """
    I2C Host's configuration with cleaning of values in properties setters.
    """

    def __init__(self, dev_i2c: ltp_i2c.I2CHost):
        self.dev_i2c: ltp_i2c.I2CHost = dev_i2c
        self.param_lim: I2CHostParameterLimits = I2CHostParameterLimits(dev_i2c=dev_i2c)


class TiePieOscilloscopeChannelConfig(PublicPropertiesReprMixin):
    """
    Oscilloscope's channel configuration, with cleaning of
    values in properties setters as well as setting and reading them on and
    from the device's channel.
    """

    def __init__(self, ch_number: int, channel: ltp_osc_ch.OscilloscopeChannel):
        self.ch_number: int = ch_number
        self.channel: ltp_osc_ch.OscilloscopeChannel = channel
        self.param_lim: OscilloscopeChannelParameterLimits = (
            OscilloscopeChannelParameterLimits(osc_channel=channel)
        )

    @staticmethod
    def clean_coupling(
        coupling: Union[str, TiePieOscilloscopeChannelCoupling]
    ) -> TiePieOscilloscopeChannelCoupling:
        return TiePieOscilloscopeChannelCoupling(coupling)

    @property  # type: ignore
    @wrap_libtiepie_exception
    def coupling(self) -> TiePieOscilloscopeChannelCoupling:
        return TiePieOscilloscopeChannelCoupling(self.channel.coupling)

    @coupling.setter
    def coupling(self, coupling: Union[str, TiePieOscilloscopeChannelCoupling]) -> None:
        self.channel.coupling = self.clean_coupling(coupling).value
        log_set("Coupling", coupling)

    @staticmethod
    def clean_enabled(enabled: bool) -> bool:
        _validate_bool("channel enabled", enabled)
        return enabled

    @property
    def enabled(self) -> bool:
        return self.channel.enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self.channel.enabled = self.clean_enabled(enabled)
        if enabled:
            msg = "enabled"
        else:
            msg = "disabled"
        log_set("Channel {}".format(self.ch_number), msg)

    def clean_input_range(
        self, input_range: Union[float, TiePieOscilloscopeRange]
    ) -> TiePieOscilloscopeRange:
        if not isinstance(input_range, TiePieOscilloscopeRange):
            _validate_number(
                "input range",
                TiePieOscilloscopeRange.suitable_range(input_range).value,
                self.param_lim.input_range,
            )
        return TiePieOscilloscopeRange.suitable_range(input_range)

    @property
    def input_range(self) -> TiePieOscilloscopeRange:
        return TiePieOscilloscopeRange(self.channel.range)

    @input_range.setter
    def input_range(self, input_range: Union[float, TiePieOscilloscopeRange]) -> None:
        self.channel.range = self.clean_input_range(input_range).value
        log_set("input range", self.channel.range, value_suffix=" V")

    def clean_probe_offset(self, probe_offset: float) -> float:
        _validate_number("probe offset", probe_offset, self.param_lim.probe_offset)
        return float(probe_offset)

    @property
    def probe_offset(self) -> float:
        return self.channel.probe_offset

    @probe_offset.setter
    def probe_offset(self, probe_offset: float) -> None:
        self.channel.probe_offset = self.clean_probe_offset(probe_offset)
        log_set("Probe offset", probe_offset)

    @property  # type: ignore
    @wrap_libtiepie_exception
    def has_safe_ground(self) -> bool:
        """
        Check whether bound oscilloscope device has "safe ground" option

        :return: bool: 1=safe ground available
        """
        return self.channel.has_safe_ground

    @staticmethod
    def clean_safe_ground_enabled(safe_ground_enabled: bool) -> bool:
        _validate_bool("safe ground enabled", safe_ground_enabled)
        return safe_ground_enabled

    @property  # type:ignore
    @wrap_libtiepie_exception
    def safe_ground_enabled(self) -> Optional[bool]:
        if not self.has_safe_ground:
            msg = "The oscilloscope has no safe ground option."
            logging.error(msg)
            raise TiePieError(msg)

        return self.channel.safe_ground_enabled

    @safe_ground_enabled.setter  # type:ignore
    @wrap_libtiepie_exception
    def safe_ground_enabled(self, safe_ground_enabled: bool) -> None:
        """
        Safe ground enable or disable

        :param safe_ground_enabled: enable / disable safe ground for channel
        """
        if not self.has_safe_ground:
            msg = "The oscilloscope has no safe ground option."
            raise TiePieError(msg)

        self.channel.safe_ground_enabled = self.clean_safe_ground_enabled(
            safe_ground_enabled
        )
        if safe_ground_enabled:
            msg = "enabled"
        else:
            msg = "disabled"
        log_set("Safe ground", msg)

    def clean_trigger_hysteresis(self, trigger_hysteresis: float) -> float:
        _validate_number(
            "trigger hysteresis", trigger_hysteresis, self.param_lim.trigger_hysteresis
        )
        return float(trigger_hysteresis)

    @property
    def trigger_hysteresis(self) -> float:
        return self.channel.trigger.hystereses[0]

    @trigger_hysteresis.setter
    def trigger_hysteresis(self, trigger_hysteresis: float) -> None:
        self.channel.trigger.hystereses[0] = self.clean_trigger_hysteresis(
            trigger_hysteresis
        )
        log_set("Trigger hysteresis", trigger_hysteresis)

    @staticmethod
    def clean_trigger_kind(
        trigger_kind: Union[str, TiePieOscilloscopeTriggerKind]
    ) -> TiePieOscilloscopeTriggerKind:
        return TiePieOscilloscopeTriggerKind(trigger_kind)

    @property
    def trigger_kind(self) -> TiePieOscilloscopeTriggerKind:
        return TiePieOscilloscopeTriggerKind(self.channel.trigger.kind)

    @trigger_kind.setter
    def trigger_kind(
        self, trigger_kind: Union[str, TiePieOscilloscopeTriggerKind]
    ) -> None:
        self.channel.trigger.kind = self.clean_trigger_kind(trigger_kind).value
        log_set("Trigger kind", trigger_kind)

    @staticmethod
    def clean_trigger_level_mode(
        level_mode: Union[str, TiePieOscilloscopeTriggerLevelMode]
    ) -> TiePieOscilloscopeTriggerLevelMode:
        return TiePieOscilloscopeTriggerLevelMode(level_mode)

    @property
    def trigger_level_mode(self) -> TiePieOscilloscopeTriggerLevelMode:
        return TiePieOscilloscopeTriggerLevelMode(self.channel.trigger.level_mode)

    @trigger_level_mode.setter
    def trigger_level_mode(
        self, level_mode: Union[str, TiePieOscilloscopeTriggerLevelMode]
    ) -> None:
        self.channel.trigger.level_mode = self.clean_trigger_level_mode(
            level_mode
        ).value
        log_set("Level mode", level_mode)

    def clean_trigger_level(self, trigger_level: float) -> float:
        if self.channel.trigger.level_mode == 1:  # RELATIVE
            _validate_number(
                "trigger level", trigger_level, self.param_lim.trigger_level_rel, float
            )
        if self.channel.trigger.level_mode == 2:  # ABSOLUTE
            _validate_number(
                "trigger level", trigger_level, self.param_lim.trigger_level_abs, float
            )
        return float(trigger_level)

    @property
    def trigger_level(self) -> float:
        return self.channel.trigger.levels[0]

    @trigger_level.setter
    def trigger_level(self, trigger_level: float) -> None:
        self.channel.trigger.levels[0] = self.clean_trigger_level(trigger_level)
        log_set("Trigger level", trigger_level, value_suffix=" V")

    @staticmethod
    def clean_trigger_enabled(trigger_enabled):
        _validate_bool("Trigger enabled", trigger_enabled)
        return trigger_enabled

    @property
    def trigger_enabled(self) -> bool:
        return self.channel.trigger.enabled

    @trigger_enabled.setter
    def trigger_enabled(self, trigger_enabled: bool) -> None:
        self.channel.trigger.enabled = self.clean_trigger_enabled(trigger_enabled)
        if trigger_enabled:
            msg = "enabled"
        else:
            msg = "disabled"
        log_set("Trigger", msg)


def _require_dev_handle(device_type):
    """
    Create method decorator to check if the TiePie device handle is available.

    :param device_type: the TiePie device type which device handle is required
    :raises ValueError: when `device_type` is not an instance of `TiePieDeviceType`
    """

    device_type: TiePieDeviceType = TiePieDeviceType(device_type)

    def wrapper(method):
        """
        Method decorator to check if a TiePie device handle is available; raises
        `TiePieError` if hand is not available.

        :param method: `TiePieDevice` instance method to wrap
        :return: Whatever wrapped `method` returns
        """

        @wraps(method)
        def wrapped_func(self, *args, **kwargs):
            dev_str = None
            if device_type is TiePieDeviceType.OSCILLOSCOPE and self._osc is None:
                dev_str = "oscilloscope"
            if device_type is TiePieDeviceType.GENERATOR and self._gen is None:
                dev_str = "generator"
            if device_type is TiePieDeviceType.I2C and self._i2c is None:
                dev_str = "I2C host"
            if dev_str is not None:
                msg = f"The {dev_str} handle is not available; call `.start()` first."
                logging.error(msg)
                raise TiePieError(msg)
            return method(self, *args, **kwargs)

        return wrapped_func

    return wrapper


class TiePieOscilloscope(SingleCommDevice):
    """
    TiePie oscilloscope.

    A wrapper for TiePie oscilloscopes, based on the class
    `libtiepie.osilloscope.Oscilloscope` with simplifications for starting of the
    device (using serial number) and managing mutable configuration of both the
    device and its channels, including extra validation and typing hints support for
    configurations.

    Note that, in contrast to `libtiepie` library, since all physical TiePie devices
    include an oscilloscope, this is the base class for all physical TiePie devices.
    The additional TiePie sub-devices: "Generator" and "I2CHost", are mixed-in to this
    base class in subclasses.

    The channels use `1..N` numbering (not `0..N-1`), as in, e.g., the Multi Channel
    software.
    """

    @staticmethod
    def config_cls() -> Type[TiePieDeviceConfig]:
        return TiePieDeviceConfig

    @staticmethod
    def default_com_cls() -> Type[NullCommunicationProtocol]:
        return NullCommunicationProtocol

    def __init__(self, com, dev_config) -> None:
        """
        Constructor for a TiePie device.
        """
        super().__init__(com, dev_config)

        self._osc: Optional[ltp_osc.Oscilloscope] = None

        self.config_osc: Optional[TiePieOscilloscopeConfig] = None
        """
        Oscilloscope's dynamical configuration.
        """

        self.config_osc_channel_dict: Dict[int, TiePieOscilloscopeChannelConfig] = {}
        """
        Channel configuration.
        A `dict` mapping actual channel number, numbered `1..N`, to channel
        configuration. The channel info is dynamically read from the device only on
        the first `start()`; beforehand the `dict` is empty.
        """

    @_require_dev_handle(TiePieDeviceType.OSCILLOSCOPE)
    def _osc_config_setup(self) -> None:
        """
        Setup dynamical configuration for the connected oscilloscope.
        """
        assert self._osc is not None
        self.config_osc = TiePieOscilloscopeConfig(
            dev_osc=self._osc,
        )
        for n in range(1, self.n_channels + 1):
            self.config_osc_channel_dict[n] = TiePieOscilloscopeChannelConfig(
                ch_number=n,
                channel=self._osc.channels[n - 1],
            )

    def _osc_config_teardown(self) -> None:
        """
        Teardown dynamical configuration for the oscilloscope.
        """
        self.config_osc = None
        self.config_osc_channel_dict = {}

    def _osc_close(self) -> None:
        """
        Close the wrapped `libtiepie` oscilloscope.
        """
        if self._osc is not None:
            del self._osc
            self._osc = None

    def _get_device_by_serial_number(
        self,
        # Note: TiePieDeviceType aenum as a tuple to define a return value type
        ltp_device_type: Tuple[int, _LtpDeviceReturnType],
    ) -> _LtpDeviceReturnType:
        """
        Wrapper around `get_device_by_serial_number` using this device's config options.

        :return: A `libtiepie` device object specific to a class it is called on.
        """
        return get_device_by_serial_number(
            self.config.serial_number,
            ltp_device_type,
            n_max_try_get_device=self.config.n_max_try_get_device,
            wait_sec_retry_get_device=self.config.wait_sec_retry_get_device,
        )

    @wrap_libtiepie_exception
    def start(self) -> None:  # type: ignore
        """
        Start the oscilloscope.
        """
        logging.info(f"Starting {self}")
        super().start()
        logging.info("Starting oscilloscope")

        self._osc = self._get_device_by_serial_number(TiePieDeviceType.OSCILLOSCOPE)

        # Check for block measurement support if required
        if self.config.require_block_measurement_support and not (
            self._osc.measure_modes & ltp.MM_BLOCK  # type: ignore
        ):
            self._osc_close()
            msg = (
                f"Oscilloscope with serial number {self.config.serial_number} does not "
                f"have required block measurement support."
            )
            logging.error(msg)
            raise TiePieError(msg)

        self._osc_config_setup()

    @wrap_libtiepie_exception
    def stop(self) -> None:  # type: ignore
        """
        Stop the oscilloscope.
        """
        logging.info(f"Stopping {self}")
        logging.info("Stopping oscilloscope")

        self._osc_config_teardown()
        self._osc_close()

        super().stop()

    @staticmethod
    @wrap_libtiepie_exception
    def list_devices() -> ltp.devicelist.DeviceList:
        """
        List available TiePie devices.

        :return: libtiepie up to date list of devices
        """
        ltp.device_list.update()
        device_list = ltp.device_list

        # log devices list
        if device_list:
            logging.info("Available devices:\n")

            for item in ltp.device_list:
                logging.info("  Name:              " + item.name)
                logging.info("  Serial number:     " + str(item.serial_number))
                logging.info("  Available types:   " + ltp.device_type_str(item.types))

        else:
            logging.info("No devices found!")

        return device_list

    @wrap_libtiepie_exception
    @_require_dev_handle(TiePieDeviceType.OSCILLOSCOPE)
    def measure(self) -> Union[List[array.array], List[np.ndarray]]:
        """
        Measures using set configuration.

        :return: Measurement data of only enabled channels in a `list` of either
            `numpy.ndarray` or `array.array` (fallback) with float sample data. The
            returned `list` items correspond to data from channel numbers as
            returned by `self.channels_enabled`.
        :raises TiePieError: when device is not started or status of underlying device
            gives an error
        """
        # make mypy happy w/ assert; `is None` check is already done in the
        # `_require_started` method decorator
        assert self._osc is not None
        self._osc.start()
        while not self._osc.is_data_ready:
            # 10 ms delay to save CPU time
            time.sleep(0.01)  # pragma: no cover
        data = self._osc.get_data()
        # filter-out disabled channels entries
        data = [ch_data for ch_data in data if ch_data is not None]
        if _has_numpy:
            data = self._measurement_data_to_numpy_array(data)
        return data

    @staticmethod
    def _measurement_data_to_numpy_array(data: List[array.array]) -> List[np.ndarray]:
        """
        Converts the measurement data from list of `array.array` to list of
        `numpy.ndarray`.

        :param data: measurement data for enabled channels as a `list` of `array.array`
        :return: measurement data for enabled channels as a `list` of `numpy.ndarray`
        :raises ImportError: when `numpy` is not available
        """
        if not _has_numpy:
            raise ImportError("numpy is required to do this")
        return [np.array(ch_data) for ch_data in data]

    @property  # type: ignore
    @_require_dev_handle(TiePieDeviceType.OSCILLOSCOPE)
    @wrap_libtiepie_exception
    def n_channels(self):
        """
        Number of channels in the oscilloscope.

        :return: Number of channels.
        """
        return len(self._osc.channels)

    @property
    def channels_enabled(self) -> Generator[int, None, None]:
        """
        Yield numbers of enabled channels.

        :return: Numbers of enabled channels
        """
        for (ch_nr, ch_config) in self.config_osc_channel_dict.items():
            if ch_config.enabled:
                yield ch_nr


class TiePieGeneratorMixin:
    """
    TiePie Generator sub-device.

    A wrapper for the `libtiepie.generator.Generator` class. To be mixed in with
    `TiePieOscilloscope` base class.
    """

    def __init__(self, com, dev_config):
        super().__init__(com, dev_config)
        self._gen: Optional[ltp_gen.Generator] = None

        self.config_gen: Optional[TiePieGeneratorConfig] = None
        """
        Generator's dynamical configuration.
        """

    @_require_dev_handle(TiePieDeviceType.GENERATOR)
    def _gen_config_setup(self) -> None:
        """
        Setup dynamical configuration for the connected generator.
        """
        self.config_gen = TiePieGeneratorConfig(
            dev_gen=self._gen,
        )

    def _gen_config_teardown(self) -> None:
        self.config_gen = None

    def _gen_close(self) -> None:
        if self._gen is not None:
            del self._gen
            self._gen = None

    def start(self) -> None:
        """
        Start the Generator.
        """
        super().start()  # type: ignore
        logging.info("Starting generator")

        self._gen = cast(TiePieOscilloscope, self)._get_device_by_serial_number(
            TiePieDeviceType.GENERATOR)
        self._gen_config_setup()

    @wrap_libtiepie_exception
    def stop(self) -> None:
        """
        Stop the generator.
        """
        logging.info("Stopping generator")

        self._gen_config_teardown()
        self._gen_close()

        super().stop()  # type: ignore

    @wrap_libtiepie_exception
    @_require_dev_handle(TiePieDeviceType.GENERATOR)
    def generator_start(self):
        """
        Start signal generation.
        """
        self._gen.start()
        logging.info("Starting signal generation")

    @wrap_libtiepie_exception
    @_require_dev_handle(TiePieDeviceType.GENERATOR)
    def generator_stop(self):
        """
        Stop signal generation.
        """
        self._gen.stop()
        logging.info("Stopping signal generation")


class TiePieI2CHostMixin:
    """
    TiePie I2CHost sub-device.

    A wrapper for the `libtiepie.i2chost.I2CHost` class. To be mixed in with
    `TiePieOscilloscope` base class.
    """

    def __init__(self, com, dev_config):
        super().__init__(com, dev_config)
        self._i2c: Optional[ltp_i2c.I2CHost] = None

        self.config_i2c: Optional[TiePieI2CHostConfig] = None
        """
        I2C host's dynamical configuration.
        """

    @_require_dev_handle(TiePieDeviceType.I2C)
    def _i2c_config_setup(self) -> None:
        """
        Setup dynamical configuration for the connected I2C host.
        """
        self.config_i2c = TiePieI2CHostConfig(
            dev_i2c=self._i2c,
        )

    def _i2c_config_teardown(self) -> None:
        """
        Teardown dynamical configuration for the I2C Host.
        """
        self.config_i2c = None

    def _i2c_close(self) -> None:
        if self._i2c is not None:
            del self._i2c
            self._i2c = None

    def start(self) -> None:
        """
        Start the I2C Host.
        """
        super().start()  # type: ignore
        logging.info("Starting I2C host")

        self._i2c = cast(TiePieOscilloscope, self)._get_device_by_serial_number(
            TiePieDeviceType.I2C)
        self._i2c_config_setup()

    @wrap_libtiepie_exception
    def stop(self) -> None:
        """
        Stop the I2C host.
        """
        logging.info("Stopping I2C host")

        self._i2c_config_teardown()
        self._i2c_close()

        super().stop()  # type: ignore


class TiePieWS5(TiePieI2CHostMixin, TiePieGeneratorMixin, TiePieOscilloscope):
    """
    TiePie WS5 device.
    """


class TiePieHS5(TiePieI2CHostMixin, TiePieGeneratorMixin, TiePieOscilloscope):
    """
    TiePie HS5 device.
    """


class TiePieHS6(TiePieOscilloscope):
    """
    TiePie HS6 DIFF device.
    """
