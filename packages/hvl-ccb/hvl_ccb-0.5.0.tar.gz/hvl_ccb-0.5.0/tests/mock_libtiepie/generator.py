#  Copyright (c) 2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Mock Generator
"""
import libtiepie.const as const
from libtiepie.generator import Generator as LtpGenerator

from hvl_ccb.dev import (
    TiePieGeneratorSignalType,
)


class Generator(LtpGenerator):
    """"""

    def __init__(self, serial_number):
        self._serial_number = serial_number

        self._frequency = None
        self._amplitude = None
        self._offset = None
        self._signal_type = const.ST_UNKNOWN
        self._enabled = None

        # add physical device parameters
        self._frequency_max = 40e6
        self._amplitude_max = 20
        self._offset_max = 10

    def _get_frequency_max(self):
        return self._frequency_max

    def _get_amplitude_max(self):
        return self._amplitude_max

    def _get_offset_max(self):
        return self._offset_max

    def _set_frequency(self, value):
        self._frequency = value

    def _get_frequency(self):
        return self._frequency

    def verify_frequency(self, value):
        return value

    def _set_amplitude(self, value):
        self._amplitude = value

    def _get_amplitude(self):
        return self._amplitude

    def verify_amplitude(self, value):
        return value

    def _set_offset(self, value):
        self._offset = value

    def _get_offset(self):
        return self._offset

    def verify_offset(self, value):
        return value

    def _set_signal_type(self, value):
        if value == 1:
            self._signal_type = TiePieGeneratorSignalType.SINE

    def _get_signal_type(self):
        return self._signal_type

    def _set_enabled(self, value):
        self._enabled = value

    def _get_enabled(self):
        return self._enabled

    def start(self):
        pass

    def stop(self):
        pass

    frequency_max = property(_get_frequency_max)
    amplitude_max = property(_get_amplitude_max)
    offset_max = property(_get_offset_max)
    frequency = property(_get_frequency, _set_frequency)
    amplitude = property(_get_amplitude, _set_amplitude)
    offset = property(_get_offset, _set_offset)
    signal_type = property(_get_signal_type, _set_signal_type)
    enabled = property(_get_enabled, _set_enabled)
