#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Test module for the supercube constants enums.
"""

import pytest

from hvl_ccb.dev.supercube import constants


def test_support_output():
    assert constants.GeneralSupport.output(1, 1) == constants.GeneralSupport.out_1_1
    assert constants.GeneralSupport.output(5, 2) == constants.GeneralSupport.out_5_2
    with pytest.raises(ValueError):
        constants.GeneralSupport.output(3, 3)


def test_support_input():
    assert constants.GeneralSupport.input(1, 1) == constants.GeneralSupport.in_1_1
    assert constants.GeneralSupport.input(5, 2) == constants.GeneralSupport.in_5_2
    with pytest.raises(ValueError):
        constants.GeneralSupport.input(3, 3)


def test_measurements_scaled_input():
    assert (constants.MeasurementsScaledInput.input(1) ==
            constants.MeasurementsScaledInput.input_1)
    assert (constants.MeasurementsScaledInput.input(3) ==
            constants.MeasurementsScaledInput.input_3)
    for n in (0, 5):
        with pytest.raises(ValueError):
            constants.MeasurementsScaledInput.input(n)


def test_measurements_divider_ratio():
    assert (constants.MeasurementsDividerRatio.input(1) ==
            constants.MeasurementsDividerRatio.input_1)
    assert (constants.MeasurementsDividerRatio.input(3) ==
            constants.MeasurementsDividerRatio.input_3)
    for n in (0, 5):
        with pytest.raises(ValueError):
            constants.MeasurementsDividerRatio.input(n)


def test_earthing_stick_status():
    assert (constants.EarthingStick.status(3) ==
            constants.EarthingStick.status_3)
    with pytest.raises(AttributeError):
        constants.MeasurementsDividerRatio.status(7)


def test_earthing_stick_manual():
    assert (constants.EarthingStick.manual(2) ==
            constants.EarthingStick.manual_2)
    with pytest.raises(ValueError):
        constants.EarthingStick.manual(7)


def test_alarms():
    assert constants.Alarms.Alarm(33) == constants.Alarms.Alarm33
    for n in (0, 152):
        with pytest.raises(ValueError):
            constants.Alarms.Alarm(n)


def test_door():
    assert constants.Door.status(3) == constants.Door.status_3
    for n in (0, 4):
        with pytest.raises(ValueError):
            constants.Door.status(n)


def test_alarm_text():
    assert constants.AlarmText.get(1) == constants.AlarmText.Alarm1
    assert constants.AlarmText.get(1000) == constants.AlarmText.not_defined


def test_message_board():
    assert constants.MessageBoard.line(3) == constants.MessageBoard.line_3
    for n in (0, 16):
        with pytest.raises(ValueError):
            constants.MessageBoard.line(n)
