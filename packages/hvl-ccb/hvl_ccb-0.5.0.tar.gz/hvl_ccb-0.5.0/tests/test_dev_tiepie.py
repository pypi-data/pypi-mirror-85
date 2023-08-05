#  Copyright (c) 2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for TiePie
"""

import sys

import pytest
from libtiepie.exceptions import LibTiePieException, InvalidDeviceSerialNumberError
from pytest_mock import MockerFixture

from hvl_ccb.dev import (
    TiePieError,
    TiePieDeviceType,
    TiePieOscilloscope,
    TiePieWS5,
    TiePieHS6,
    TiePieHS5,
    TiePieOscilloscopeResolution,
    TiePieOscilloscopeChannelCoupling,
    TiePieOscilloscopeTriggerKind,
    TiePieOscilloscopeRange,
    TiePieOscilloscopeTriggerLevelMode,
    TiePieGeneratorSignalType,
    TiePieOscilloscopeAutoResolutionModes,
    TiePieDeviceConfig,
)
from hvl_ccb.dev.tiepie import (
    get_device_by_serial_number,
    _verify_via_libtiepie,
    _validate_number,
    TiePieGeneratorMixin,
    TiePieI2CHostMixin,
)
from tests.mock_libtiepie.const import (
    MOCK_I2CHOST_SERIAL_NUMBER,
    MOCK_GENERATOR_SERIAL_NUMBER,
    MOCK_OSCILLOSCOPE_SERIAL_NUMBER,
    MOCK_OSCILLOSCOPE_SERIAL_NUMBER_2,
    MOCK_DEVICE_SERIAL_NUMBER,
)

"""
Mocking libtiepie
"""
from tests.mock_libtiepie import oscilloscope as _oscilloscope  # noqa: E402
from tests.mock_libtiepie import generator as _generator  # noqa: E402
from tests.mock_libtiepie import i2chost as _i2chost  # noqa: E402
from tests.mock_libtiepie.devicelist import device_list as _device_list  # noqa: E402

libtiepie = sys.modules["libtiepie"]

libtiepie.device_list = _device_list
libtiepie.oscilloscope = _oscilloscope
libtiepie.generator = _generator
libtiepie.i2chost = _i2chost

sys.modules["libtiepie"] = libtiepie


@pytest.fixture(scope="module")
def com_config():
    return {}


@pytest.fixture(scope="module")
def dev_config():
    return {
        "serial_number": MOCK_DEVICE_SERIAL_NUMBER,
        "n_max_try_get_device": 2,
        "wait_sec_retry_get_device": 0.01,
    }


def test_instantiation(com_config, dev_config):
    dev_hs6 = TiePieHS6(com_config, dev_config)
    assert dev_hs6 is not None
    dev_hs5 = TiePieHS5(com_config, dev_config)
    assert dev_hs5 is not None
    dev_ws5 = TiePieWS5(com_config, dev_config)
    assert dev_ws5 is not None


def test_wrap_libtiepie_exception(com_config, dev_config, mocker: MockerFixture):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    def raise_libtiepie_exception():
        raise LibTiePieException(0, "mock")

    mocker.patch(
        "libtiepie.device_list.update",
        side_effect=raise_libtiepie_exception,
        autospec=True,
    )

    with pytest.raises(TiePieError):
        dev_osc.list_devices()

    with pytest.raises(TiePieError):
        get_device_by_serial_number(
            dev_osc.config.serial_number, TiePieDeviceType.OSCILLOSCOPE
        )

    with pytest.raises(TiePieError):
        dev_osc.start()


def test_list_devices(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)
    list_devices = dev_osc.list_devices()
    assert list_devices is not None


def test_list_devices_none_available(com_config, dev_config, mocker: MockerFixture):
    # simulate absence of devices
    mock_devices = mocker.patch.object(libtiepie.device_list, "mock_devices")
    mock_devices.return_value = False

    dev_osc = TiePieOscilloscope(com_config, dev_config)
    list_devices = dev_osc.list_devices()
    assert not list_devices


def test_get_device_by_serial_number():
    dev_osc = get_device_by_serial_number(
        MOCK_OSCILLOSCOPE_SERIAL_NUMBER,
        TiePieDeviceType.OSCILLOSCOPE,
    )
    assert dev_osc is not None

    dev_gen = get_device_by_serial_number(
        MOCK_GENERATOR_SERIAL_NUMBER,
        TiePieDeviceType.GENERATOR,
    )
    assert dev_gen is not None

    dev_i2c = get_device_by_serial_number(
        MOCK_I2CHOST_SERIAL_NUMBER,
        TiePieDeviceType.I2C,
    )
    assert dev_i2c is not None


@pytest.mark.parametrize(
    "wrong_dev_config",
    [
        {"serial_number": -23},
        {"n_max_try_get_device": 0},
        {"wait_sec_retry_get_device": 0.0},
    ],
)
def test_invalid_config_dict(dev_config, wrong_dev_config):
    invalid_config = dict(dev_config)
    invalid_config.update(wrong_dev_config)
    with pytest.raises(ValueError):
        TiePieDeviceConfig(**invalid_config)


def test_get_device_by_serial_number_not_available(dev_config, mocker: MockerFixture):
    # simulate absence of devices
    mock_devices = mocker.patch.object(libtiepie.device_list, "mock_devices")
    mock_devices.return_value = False

    with pytest.raises(TiePieError):
        get_device_by_serial_number(
            MOCK_OSCILLOSCOPE_SERIAL_NUMBER,
            TiePieDeviceType.OSCILLOSCOPE,
            n_max_try_get_device=dev_config["n_max_try_get_device"],
            wait_sec_retry_get_device=dev_config["wait_sec_retry_get_device"],
        )


def test_get_device_by_serial_number_wrong_device_type():
    with pytest.raises(TiePieError):
        get_device_by_serial_number(
            MOCK_GENERATOR_SERIAL_NUMBER,
            TiePieDeviceType.OSCILLOSCOPE,
        )


def test_get_device_by_serial_number_invalid_device_sn(
    dev_config,
    mocker: MockerFixture,
):
    # simulate invalid device serian number error
    get_item_by_serial_number = mocker.patch.object(
        libtiepie.device_list,
        "get_item_by_serial_number",
    )
    get_item_by_serial_number.side_effect = InvalidDeviceSerialNumberError

    with pytest.raises(TiePieError):
        get_device_by_serial_number(
            MOCK_OSCILLOSCOPE_SERIAL_NUMBER,
            TiePieDeviceType.OSCILLOSCOPE,
            n_max_try_get_device=dev_config["n_max_try_get_device"],
            wait_sec_retry_get_device=dev_config["wait_sec_retry_get_device"],
        )


def test_block_measurement_support():
    dev_osc = TiePieOscilloscope(
        {},
        {"serial_number": MOCK_OSCILLOSCOPE_SERIAL_NUMBER_2},
    )

    with pytest.raises(TiePieError):
        dev_osc.start()


def test_channel_config_on_start_stop(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    assert not dev_osc.config_osc_channel_dict
    # with pytest.raises(TiePieError):
    #     dev_osc.n_channels

    dev_osc.start()

    n_channels = dev_osc.n_channels

    for ch_nr in range(1, n_channels + 1):
        assert ch_nr in dev_osc.config_osc_channel_dict
        assert not dev_osc.config_osc_channel_dict[ch_nr].enabled

    for wrong_ch_nr in (0, dev_osc.n_channels + 1):
        with pytest.raises(KeyError):
            dev_osc.config_osc_channel_dict[wrong_ch_nr]

    dev_osc.stop()


def test_channels_enabled(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)
    dev_osc.start()
    for ch_config in dev_osc.config_osc_channel_dict.values():
        ch_config.enabled = True
    assert list(dev_osc.channels_enabled) == list(
        dev_osc.config_osc_channel_dict.keys()
    )
    dev_osc.stop()


def test_n_channels(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)
    dev_osc.start()
    assert dev_osc.n_channels == 3
    dev_osc.stop()


def test_dev_osc_not_running(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)
    with pytest.raises(TiePieError):
        dev_osc.n_channels == 3

    class TiePieGeneratorOscilloscope(TiePieGeneratorMixin, TiePieOscilloscope):
        pass

    dev_gen = TiePieGeneratorOscilloscope(com_config, dev_config)
    with pytest.raises(TiePieError):
        dev_gen.generator_start()

    class TiePieI2CHostOscilloscope(TiePieI2CHostMixin, TiePieOscilloscope):
        pass
    dev_i2c = TiePieI2CHostOscilloscope(com_config, dev_config)

    with pytest.raises(TiePieError):
        dev_i2c._i2c_config_setup()  # ATM only priv method avail for testing


def test_safe_ground_enabled(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    dev_osc.start()

    for ch_nr, ch_config in dev_osc.config_osc_channel_dict.items():
        assert ch_config.safe_ground_enabled is False

    for ch_nr in [1, 3]:
        dev_osc.config_osc_channel_dict[ch_nr].safe_ground_enabled = True
    for ch_nr in [2]:
        assert dev_osc.config_osc_channel_dict[ch_nr].safe_ground_enabled is False

    dev_osc.stop()


def test_safe_ground_not_available(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    dev_osc.start()

    for ch_nr, ch_config in dev_osc.config_osc_channel_dict.items():
        ch_config.channel.disable_safe_ground_option()

    for ch_nr, ch_config in dev_osc.config_osc_channel_dict.items():
        with pytest.raises(TiePieError):
            dev_osc.config_osc_channel_dict[ch_nr].safe_ground_enabled = True
        with pytest.raises(TiePieError):
            dev_osc.config_osc_channel_dict[ch_nr].safe_ground_enabled

    dev_osc.stop()


def test_trigger_enabled(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    for ch_nr, ch_config in dev_osc.config_osc_channel_dict.items():
        ch_config.trigger_enabled = False
        assert ch_config.trigger_enabled is False

    dev_osc.start()

    for ch_nr, ch_config in dev_osc.config_osc_channel_dict.items():
        assert ch_config.trigger_enabled is False

    for ch_nr in [1, 3]:
        dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled = True
        assert dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled is True

    for ch_nr in [2]:
        assert dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled is False

    for ch_nr in [3]:
        dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled = False

    for ch_nr in [1]:
        assert dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled is True

    for ch_nr in [2, 3]:
        assert dev_osc.config_osc_channel_dict[ch_nr].trigger_enabled is False

    dev_osc.stop()


def test_scope_config_set(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    assert dev_osc.config_osc is None

    dev_osc.start()

    config_osc = dev_osc.config_osc

    # record length
    record_length_value = 100
    config_osc.record_length = record_length_value
    assert config_osc.record_length == record_length_value

    # sample frequency
    sample_frequency_value = 1e6
    config_osc.sample_frequency = sample_frequency_value
    assert config_osc.sample_frequency == sample_frequency_value

    # pre-sample ratio
    pre_sample_ratio_value = 0.2
    config_osc.pre_sample_ratio = pre_sample_ratio_value
    assert config_osc.pre_sample_ratio == pre_sample_ratio_value

    # resolution
    resolution = TiePieOscilloscopeResolution.FOURTEEN_BIT
    config_osc.resolution = resolution
    assert config_osc.resolution == resolution

    # trigger time out
    trigger_time_out = 1
    config_osc.trigger_time_out = trigger_time_out
    assert config_osc.trigger_time_out == trigger_time_out

    # auto resolution mode
    auto_resolution_mode = TiePieOscilloscopeAutoResolutionModes.DISABLED
    config_osc.auto_resolution_mode = auto_resolution_mode
    assert config_osc.auto_resolution_mode == auto_resolution_mode

    dev_osc.stop()

    assert dev_osc.config_osc is None


def test_scope_config_set_invalid(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    dev_osc.start()

    config_osc = dev_osc.config_osc

    # sample_frequency
    with pytest.raises(ValueError):
        config_osc.sample_frequency = -1
    with pytest.raises(ValueError):
        config_osc.sample_frequency = 1e14
    with pytest.raises(TypeError):
        config_osc.sample_frequency = "1"

    # record_length
    with pytest.raises(ValueError):
        config_osc.record_length = -1
    with pytest.raises(TypeError):
        config_osc.record_length = "1"

    # pre_sample_ratio
    for v in (-0.1, 1.1):
        with pytest.raises(ValueError):
            config_osc.pre_sample_ratio = v
    with pytest.raises(TypeError):
        config_osc.pre_sample_ratio = "0.5"

    # resolution
    with pytest.raises(ValueError):
        config_osc.resolution = 1
    with pytest.raises(TypeError):
        config_osc.resolution = "8"

    # trigger_time_out
    with pytest.raises(ValueError):
        config_osc.trigger_time_out = -0.1
    with pytest.raises(TypeError):
        config_osc.trigger_time_out = "123"

    # auto resolution mode
    with pytest.raises(TypeError):
        config_osc.auto_resolution_mode = False
    with pytest.raises(TypeError):
        config_osc.auto_resolution_mode = "Disabled"


def test_channel_config_set(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    assert not dev_osc.config_osc_channel_dict

    dev_osc.start()

    assert dev_osc.config_osc_channel_dict

    # Channel 2
    ch2_config = dev_osc.config_osc_channel_dict[2]

    # coupling
    coupling_value = TiePieOscilloscopeChannelCoupling.ACV
    ch2_config.coupling = coupling_value
    assert ch2_config.coupling == coupling_value

    ch2_config.coupling = "ACV"
    assert ch2_config.coupling is TiePieOscilloscopeChannelCoupling.ACV

    # enabled
    enabled_value = True
    ch2_config.enabled = enabled_value
    assert ch2_config.enabled == enabled_value

    # range
    range_value = TiePieOscilloscopeRange.TWENTY_VOLT
    ch2_config.input_range = range_value
    assert ch2_config.input_range == range_value

    for v, ir in (
        (20, TiePieOscilloscopeRange.TWENTY_VOLT),
        (21, TiePieOscilloscopeRange.FORTY_VOLT),
        (123456789, TiePieOscilloscopeRange.EIGHTY_VOLT),
    ):
        ch2_config.input_range = v
        assert ch2_config.input_range is ir

    # probe offset
    probe_offset_value = 1
    ch2_config.probe_offset = probe_offset_value
    assert ch2_config.probe_offset == probe_offset_value

    # safe ground enabled
    ch2_config.channel.enable_safe_ground_option()
    safe_ground_enabled_value = True
    ch2_config.safe_ground_enabled = safe_ground_enabled_value
    assert ch2_config.safe_ground_enabled == safe_ground_enabled_value
    ch2_config.safe_ground_enabled = False
    assert ch2_config.safe_ground_enabled is False

    # trigger level mode
    trigger_level_mode_value = TiePieOscilloscopeTriggerLevelMode.ABSOLUTE
    ch2_config.trigger_level_mode = trigger_level_mode_value
    assert ch2_config.trigger_level_mode == trigger_level_mode_value

    # trigger level
    trigger_level_value = 0.5
    ch2_config.trigger_level = trigger_level_value
    assert ch2_config.trigger_level == trigger_level_value

    # trigger level mode
    trigger_level_mode_value = TiePieOscilloscopeTriggerLevelMode.RELATIVE
    ch2_config.trigger_level_mode = trigger_level_mode_value
    assert ch2_config.trigger_level_mode == trigger_level_mode_value

    # trigger level
    trigger_level_value = 0.5
    ch2_config.trigger_level = trigger_level_value
    assert ch2_config.trigger_level == trigger_level_value

    # trigger hysteresis
    trigger_hysteresis_value = 0.05
    ch2_config.trigger_hysteresis = trigger_hysteresis_value
    assert ch2_config.trigger_hysteresis == trigger_hysteresis_value

    # trigger kind
    trigger_kind_value = TiePieOscilloscopeTriggerKind.RISING_OR_FALLING
    ch2_config.trigger_kind = trigger_kind_value
    assert ch2_config.trigger_kind == trigger_kind_value

    ch2_config.trigger_kind = "FALLING"
    assert ch2_config.trigger_kind is TiePieOscilloscopeTriggerKind.FALLING

    # trigger enabled
    trigger_enabled_value = True
    ch2_config.trigger_enabled = trigger_enabled_value
    assert ch2_config.trigger_enabled == trigger_enabled_value

    dev_osc.stop()

    assert not dev_osc.config_osc_channel_dict


def test_channel_config_set_invalid(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    assert not dev_osc.config_osc_channel_dict

    dev_osc.start()

    # Channel 2
    ch_config = dev_osc.config_osc_channel_dict[2]

    # coupling
    for v in ("dcv", 123):
        with pytest.raises(ValueError):
            ch_config.coupling = v

    # enabled
    for v in ("True", 1):
        with pytest.raises(TypeError):
            ch_config.enabled = v

    # input_range
    with pytest.raises(TypeError):
        ch_config.input_range = "40"

    # probe_offset
    for v in (-1e7, 1e7):
        with pytest.raises(ValueError):
            ch_config.probe_offset = v
    with pytest.raises(TypeError):
        ch_config.probe_offset = "1"

    # safe_ground_enabled
    for v in ("True", 1):
        with pytest.raises(TypeError):
            ch_config.safe_ground_enabled = v

    # trigger_hysteresis
    for v in (-0.1, 1.1):
        with pytest.raises(ValueError):
            ch_config.trigger_hysteresis = v
    with pytest.raises(TypeError):
        ch_config.trigger_hysteresis = "0.5"

    # trigger_kind
    for v in ("any", "Any", 123):
        with pytest.raises(ValueError):
            ch_config.trigger_kind = v

    # trigger_enabled
    for v in ("True", 1):
        with pytest.raises(TypeError):
            ch_config.trigger_enabled = v


def _test_measure_data(data):
    assert len(data) == 3
    for i, ch_data in enumerate(data):
        _test_measure_data_ch(i + 1, ch_data)


def _test_measure_data_ch(ch_nr, ch_data):
    assert len(ch_data) == ch_nr
    for i in range(ch_nr):
        assert ch_data[i] == float(i)


def _test_measure(dev_osc, has_numpy):
    # Enable all channels for measurement
    for ch in dev_osc.config_osc_channel_dict.values():
        ch.enabled = True

    # Let the oscilloscope gather data
    data = dev_osc.measure()

    if has_numpy:
        import numpy as np

        assert all(isinstance(x, np.ndarray) for x in data)

    _test_measure_data(data)

    # Disable channel 2 and measure again
    dev_osc.config_osc_channel_dict[2].enabled = False
    data = dev_osc.measure()
    assert len(data) == 2
    _test_measure_data_ch(1, data[0])
    _test_measure_data_ch(3, data[1])


def test_measure(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)

    # not running error
    with pytest.raises(TiePieError):
        dev_osc.measure()

    dev_osc.start()

    from hvl_ccb.dev.tiepie import _has_numpy

    _test_measure(dev_osc, _has_numpy)

    if _has_numpy:
        # mock no numpy and measure again
        del sys.modules["numpy"]
        import hvl_ccb

        hvl_ccb.dev.tiepie._has_numpy = False

        _test_measure(dev_osc, False)

    dev_osc.stop()


def test_generator_config_set(com_config, dev_config):
    dev_ws5 = TiePieWS5(com_config, dev_config)
    assert dev_ws5 is not None

    assert dev_ws5.config_gen is None

    dev_ws5.start()

    config_gen = dev_ws5.config_gen

    # frequency
    frequency_value = 1e6
    config_gen.frequency = frequency_value
    assert config_gen.frequency == frequency_value

    # amplitude
    amplitude_value = 2
    config_gen.amplitude = amplitude_value
    assert config_gen.amplitude == amplitude_value

    # offset
    offset_value = 1
    config_gen.offset = offset_value
    assert config_gen.offset == offset_value

    # signal type
    signal_type = TiePieGeneratorSignalType.SINE
    config_gen.signal_type = signal_type
    assert config_gen.signal_type == signal_type

    # enabled
    enabled_value = True
    config_gen.enabled = enabled_value
    assert config_gen.enabled == enabled_value
    config_gen.enabled = False
    assert config_gen.enabled is False

    dev_ws5.stop()

    assert dev_ws5.config_gen is None


def test_generator_config_set_invalid(com_config, dev_config):
    dev_ws5 = TiePieWS5(com_config, dev_config)
    assert dev_ws5 is not None

    dev_ws5.start()

    config_gen = dev_ws5.config_gen

    # frequency
    with pytest.raises(ValueError):
        config_gen.frequency = -1
    with pytest.raises(ValueError):
        config_gen.frequency = 1e14
    with pytest.raises(TypeError):
        config_gen.frequency = "1"

    # amplitude
    with pytest.raises(ValueError):
        config_gen.amplitude = -1
    with pytest.raises(ValueError):
        config_gen.amplitude = 100
    with pytest.raises(TypeError):
        config_gen.frequency = "1"

    # offset
    with pytest.raises(ValueError):
        config_gen.offset = 100
    with pytest.raises(TypeError):
        config_gen.offset = "1"

    # signal type
    with pytest.raises(ValueError):
        config_gen.signal_type = "sin"

    # enabled
    for v in ("True", 1):
        with pytest.raises(TypeError):
            config_gen.enabled = v

    dev_ws5.stop()


def test_generate_signal(com_config, dev_config):
    dev_ws5 = TiePieWS5(com_config, dev_config)
    assert dev_ws5 is not None

    dev_ws5.start()

    dev_ws5.generator_start()
    dev_ws5.generator_stop()

    dev_ws5.stop()


def test_verify_via_libtiepie():
    dev_osc = get_device_by_serial_number(
        MOCK_OSCILLOSCOPE_SERIAL_NUMBER,
        TiePieDeviceType.OSCILLOSCOPE,
    )
    assert dev_osc is not None
    assert _verify_via_libtiepie(dev_osc, "sample_frequency", 1e6) == 1e6


def test_validate_number():
    assert _validate_number("Test", 1, None, int) is None
    with pytest.raises(ValueError):
        _validate_number("Test", -1, (0, 10), int)


def test_config_print_values(com_config, dev_config):
    dev_osc = TiePieOscilloscope(com_config, dev_config)
    dev_osc.start()
    config_osc = dev_osc.config_osc
    assert f"record_length={config_osc.record_length!r}" in str(config_osc)
    config_osc.record_length = 100
    assert f"record_length={config_osc.record_length!r}" in str(config_osc)

    ch_config = dev_osc.config_osc_channel_dict[1]
    assert f"enabled={ch_config.enabled!r}" in str(ch_config)
    ch_config.enabled = not ch_config.enabled
    assert f"enabled={ch_config.enabled!r}" in str(ch_config)

    dev_ws5 = TiePieWS5(com_config, dev_config)
    dev_ws5.start()
    config_gen = dev_ws5.config_gen
    assert f"amplitude={config_gen.amplitude!r}" in str(config_gen)
    config_gen.amplitude = 12
    assert f"amplitude={config_gen.amplitude!r}" in str(config_gen)

    config_i2c = dev_ws5.config_i2c
    assert "()" in str(config_i2c)  # no config properties yet
