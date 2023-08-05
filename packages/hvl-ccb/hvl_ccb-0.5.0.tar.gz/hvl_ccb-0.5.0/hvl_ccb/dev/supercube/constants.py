#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Constants, variable names for the Supercube OPC-connected devices.
"""

from typing import cast, Sequence, Sized, Tuple

from aenum import IntEnum, EnumMeta

from hvl_ccb.utils.enum import ValueEnum, unique


@unique
class SupercubeOpcEndpoint(ValueEnum):
    """
    OPC Server Endpoint strings for the supercube variants.
    """

    A = "Supercube Typ A"
    B = "Supercube Typ B"


# NOTE: super metaclass has to match metaclass of `super(GeneralSupport)`!
class GeneralSupportMeta(EnumMeta):
    def __new__(metacls, clsname, bases, clsdict, **kwargs):
        cls = EnumMeta.__new__(
            metacls, clsname, bases, clsdict, **kwargs
        )
        # BEWARE: keep manually in sync with suffixes of enum instances; opt use dir()
        cls._port_range = range(1, 7)
        cls._contact_range = range(1, 3)
        return cls


@unique
class GeneralSupport(ValueEnum, metaclass=GeneralSupportMeta):
    """
    NodeID strings for the support inputs and outputs.
    """

    in_1_1 = '"Ix_Allg_Support1_1"'
    in_1_2 = '"Ix_Allg_Support1_2"'
    in_2_1 = '"Ix_Allg_Support2_1"'
    in_2_2 = '"Ix_Allg_Support2_2"'
    in_3_1 = '"Ix_Allg_Support3_1"'
    in_3_2 = '"Ix_Allg_Support3_2"'
    in_4_1 = '"Ix_Allg_Support4_1"'
    in_4_2 = '"Ix_Allg_Support4_2"'
    in_5_1 = '"Ix_Allg_Support5_1"'
    in_5_2 = '"Ix_Allg_Support5_2"'
    in_6_1 = '"Ix_Allg_Support6_1"'
    in_6_2 = '"Ix_Allg_Support6_2"'
    out_1_1 = '"Qx_Allg_Support1_1"'
    out_1_2 = '"Qx_Allg_Support1_2"'
    out_2_1 = '"Qx_Allg_Support2_1"'
    out_2_2 = '"Qx_Allg_Support2_2"'
    out_3_1 = '"Qx_Allg_Support3_1"'
    out_3_2 = '"Qx_Allg_Support3_2"'
    out_4_1 = '"Qx_Allg_Support4_1"'
    out_4_2 = '"Qx_Allg_Support4_2"'
    out_5_1 = '"Qx_Allg_Support5_1"'
    out_5_2 = '"Qx_Allg_Support5_2"'
    out_6_1 = '"Qx_Allg_Support6_1"'
    out_6_2 = '"Qx_Allg_Support6_2"'

    @classmethod
    def port_range(cls) -> Sequence[int]:
        """
        Integer range of all ports.

        :return: sequence of port numbers
        """
        return cls._port_range

    @classmethod
    def contact_range(cls) -> Sequence[int]:
        """
        Integer range of all contacts.

        :return: sequence of contact numbers
        """
        return cls._contact_range

    @classmethod
    def _validate_port_contact_numbers(cls, port: int, contact: int):
        """
        Validate earthing stick number.

        :param port: the port number
        :param contact: the contact number
        :raises ValueError: when port or contact number is not valid
        """
        if port not in cls.port_range():
            raise ValueError(
                f"Port number must be one of {list(cls.port_range())}"
            )
        if contact not in cls.contact_range():
            raise ValueError(
                f"Contact number must be one of {list(cls.contact_range())}"
            )

    @classmethod
    def output(cls, port: int, contact: int):
        """
        Get the NodeID string for a support output.

        :param port: the desired port (1..6)
        :param contact: the desired contact at the port (1..2)
        :return: the node id string
        :raises ValueError: when port or contact number is not valid
        """
        cls._validate_port_contact_numbers(port, contact)
        return getattr(cls, "out_{}_{}".format(port, contact))

    @classmethod
    def input(cls, port: int, contact: int):
        """
        Get the NodeID string for a support input.

        :param port: the desired port (1..6)
        :param contact: the desired contact at the port (1..2)
        :return: the node id string
        :raises ValueError: when port or contact number is not valid
        """
        cls._validate_port_contact_numbers(port, contact)
        return getattr(cls, "in_{}_{}".format(port, contact))


@unique
class BreakdownDetection(ValueEnum):
    """
    Node ID strings for the breakdown detection.

    TODO: these variable NodeIDs are not tested and/or correct yet.
    """

    #: Boolean read-only variable indicating whether breakdown detection and fast
    #: switchoff is enabled in the system or not.
    activated = '"Ix_Allg_Breakdown_activated"'

    #: Boolean read-only variable telling whether the fast switch-off has triggered.
    #: This can also be seen using the safety circuit state, therefore no method is
    #: implemented to read this out directly.
    triggered = '"Ix_Allg_Breakdown_triggered"'

    #: Boolean writable variable to reset the fast switch-off. Toggle to re-enable.
    reset = '"Qx_Allg_Breakdown_reset"'


@unique
class GeneralSockets(ValueEnum):
    """
    NodeID strings for the power sockets (3x T13 and 1xCEE16).
    """

    #: SEV T13 socket No. 1 (writable boolean).
    t13_1 = '"Qx_Allg_Socket_T13_1"'

    #: SEV T13 socket No. 2 (writable boolean).
    t13_2 = '"Qx_Allg_Socket_T13_2"'

    #: SEV T13 socket No. 3 (writable boolean).
    t13_3 = '"Qx_Allg_Socket_T13_3"'

    #: CEE16 socket (writeable boolean).
    cee16 = '"Qx_Allg_Socket_CEE16"'


T13_SOCKET_PORTS = (1, 2, 3)
"""
Port numbers of SEV T13 power socket
"""


@unique
class Safety(ValueEnum):
    """
    NodeID strings for the basic safety circuit status and green/red switches "ready"
    and "operate".
    """

    #: Status is a read-only integer containing the state number of the
    #: supercube-internal state machine. The values correspond to numbers in
    #: :class:`SafetyStatus`.
    status = '"DB_Safety_Circuit"."si_safe_status"'

    #: Writable boolean for switching to Red Ready (locked, HV off) state.
    switch_to_ready = '"DB_Safety_Circuit"."sx_safe_switch_to_ready"'

    #: Writable boolean for switching to Red Operate (locket, HV on) state.
    switch_to_operate = '"DB_Safety_Circuit"."sx_safe_switch_to_operate"'


class SafetyStatus(IntEnum):
    """
    Safety status values that are possible states returned from
    :meth:`hvl_ccb.dev.supercube.base.Supercube.get_status`. These
    values correspond to the states of the Supercube's safety circuit statemachine.
    """

    #: System is initializing or booting.
    Initializing = 0

    #: System is safe, lamps are green and some safety elements are not in place such
    #: that it cannot be switched to red currently.
    GreenNotReady = 1

    #: System is safe and all safety elements are in place to be able to switch to
    #: *ready*.
    GreenReady = 2

    #: System is locked in red state and *ready* to go to *operate* mode.
    RedReady = 3

    #: System is locked in red state and in *operate* mode, i.e. high voltage on.
    RedOperate = 4

    #: Fast turn off triggered and switched off the system. Reset FSO to go back to a
    #: normal state.
    QuickStop = 5

    #: System is in error mode.
    Error = 6


@unique
class Power(ValueEnum):
    """
    Variable NodeID strings concerning power data.

    TODO: these variable NodeIDs are not tested and/or correct yet, they don't exist
        yet on Supercube side.
    """

    #: Primary voltage in volts, measured by the frequency converter at its output.
    #: (read-only)
    voltage_primary = "Qr_Power_FU_actual_Voltage"

    #: Primary current in ampere, measured by the frequency converter. (read-only)
    current_primary = "Qr_Power_FU_actual_Current"

    #: Power setup that is configured using the Supercube HMI. The value corresponds to
    #: the ones in :class:`PowerSetup`. (read-only)
    setup = "Qi_Power_Setup"

    #: Voltage slope in V/s.
    voltage_slope = "Ir_Power_dUdt"

    #: Target voltage setpoint in V.
    voltage_target = "Ir_Power_Target_Voltage"

    #: Maximum voltage allowed by the current experimental setup. (read-only)
    voltage_max = "Iw_Power_max_Voltage"

    #: Frequency converter output frequency. (read-only)
    frequency = "Ir_Power_FU_Frequency"


class PowerSetup(IntEnum):
    """
    Possible power setups corresponding to the value of variable :attr:`Power.setup`.
    """

    #: No safety switches, use only safety components (doors, fence, earthing...)
    #: without any power.
    NoPower = 0

    #: External power supply fed through blue CEE32 input using isolation transformer
    #: and safety switches of the Supercube, or using an external safety switch
    #: attached to the Supercube Type B.
    External = 1

    #: AC voltage with MWB transformer set to 50kV maximum voltage.
    AC_SingleStage_50kV = 2

    #: AC voltage with MWB transformer set to 100kV maximum voltage.
    AC_SingleStage_100kV = 3

    #: AC voltage with two MWB transformers, one at 100kV and the other at 50kV,
    #: resulting in a total maximum voltage of 150kV.
    AC_DoubleStage_150kV = 4

    #: AC voltage with two MWB transformers both at 100kV, resulting in a total
    #: maximum voltage of 200kV
    AC_DoubleStage_200kV = 5

    #: Internal usage of the frequency converter, controlling to the primary voltage
    #: output of the supercube itself (no measurement transformer used)
    Internal = 6

    #: DC voltage with one AC transformer set to 100kV AC, resulting in 140kV DC
    DC_SingleStage_140kV = 7

    #: DC voltage with two AC transformers set to 100kV AC each, resulting in 280kV
    #: DC in total (or a single stage transformer with Greinacher voltage doubling
    #: rectifier)
    DC_DoubleStage_280kV = 8


class _PrefixedNumbersEnumBase(ValueEnum):
    """
    Base class for enums with "{prefix}{n}" instance names, where n=1..N.
    """

    @classmethod
    def range(cls) -> Sequence[int]:
        """
        Integer range of all channels.

        :return: sequence of channel numbers
        """
        return range(1, len(cast(Sized, cls))+1)

    @classmethod
    def _validate_number(cls, number: int):
        """
        Validate enum instance number.

        :param number: the enum instance number (1..N)
        :raises ValueError: when enum instance number is not in 1..N range
        """
        if number not in cls.range():
            raise ValueError(
                f"{cls._prefix()} number must be one of {list(cls.range())}"
            )

    @classmethod
    def _prefix(cls) -> str:
        """
        Enum instances name prefix: "{prefix}{n}"

        :return: enum instances prefix string
        """
        raise NotImplementedError("Implement in subclass")

    @property
    def number(self) -> int:
        """
        Get corresponding enum instance number.

        :return: enum instance number (1..N)
        """
        # Py >=3.9: self.name.removeprefix()
        return int(self.name[len(self._prefix()):])

    # no type return as it would be a arguably too complex/obscure;
    # cf. https://github.com/python/typing/issues/58#issuecomment-326240794
    @classmethod
    def get(cls, number: int):
        """
        Get the enum instance for a given number.

        :param number: the instance number (1..N)
        :return: the enum instance for the given number.
        :raises ValueError: when instance number is not in the 1..N range
        """
        cls._validate_number(number)
        return getattr(cls, f"{cls._prefix()}{number}")


class _InputEnumBase(_PrefixedNumbersEnumBase):
    """
    Base class for enums with "input_{n}" instance names, where n=1..N.
    """

    @classmethod
    def _prefix(cls) -> str:
        return "input_"

    @classmethod
    def input(cls, channel: int):
        """
        Get the enum instance for a given channel number.

        :param channel: the channel number (1..N)
        :return: the enum instance for the given channel.
        :raises ValueError: when channel number is not in the 1..N range
        """
        return cls.get(channel)


MeasurementsScaledInput = unique(_InputEnumBase(
    "MeasurementsScaledInput",
    {
        f"{_InputEnumBase._prefix()}{n}":
            f'"DB_Measurements"."si_scaled_Voltage_Input_{n}"'
        for n in range(1, 5)
    }
))
"""
Variable NodeID strings for the four analog BNC inputs for measuring voltage.
The voltage returned in these variables is already scaled with the set ratio,
which can be read using the variables in :class:`MeasurementsDividerRatio`.
"""


MeasurementsDividerRatio = unique(_InputEnumBase(
    "MeasurementsDividerRatio",
    {
        f"{_InputEnumBase._prefix()}{n}":
            f'"DB_Measurements"."si_Divider_Ratio_{n}"'
        for n in range(1, 5)
    }
))
"""
Variable NodeID strings for the measurement input scaling ratios. These ratios
are defined in the Supercube HMI setup and are provided in the python module here
to be able to read them out, allowing further calculations.
"""


class EarthingStickStatus(IntEnum):
    """
    Status of an earthing stick. These are the possible values in the status integer
    e.g. in :attr:`EarthingStick.status_1`.
    """

    #: Earthing stick is deselected and not enabled in safety circuit. To get out of
    #: this state, the earthing has to be enabled in the Supercube HMI setup.
    inactive = 0

    #: Earthing is closed (safe).
    closed = 1

    #: Earthing is open (not safe).
    open = 2

    #: Earthing is in error, e.g. when the stick did not close correctly or could not
    #: open.
    error = 3


class EarthingStickOperatingStatus(IntEnum):
    """
    Operating Status for an earthing stick. Stick can be used in auto or manual mode.
    """

    auto = 0
    manual = 1


class EarthingStickOperation(IntEnum):
    """
    Operation of the earthing stick in manual operating mode. Can be closed of opened.
    """

    open = 0
    close = 1


# NOTE: super metaclass has to match metaclass of `super(EarthingStick)`!
class EarthingStickMeta(EnumMeta):
    def __new__(metacls, clsname, bases, clsdict, **kwargs):
        cls = EnumMeta.__new__(
            metacls, clsname, bases, clsdict, **kwargs
        )
        # BEWARE: keep manually in sync with suffixes of enum instances; opt use dir()
        cls._range = range(1, 7)
        cls._statuses = tuple(
            getattr(cls, f"status_{number}") for number in cls._range
        )
        cls._manuals = tuple(
            getattr(cls, f"manual_{number}") for number in cls._range
        )
        cls._operating_statuses = tuple(
            getattr(cls, f"operating_status_{number}") for number in cls._range
        )
        return cls


@unique
class EarthingStick(ValueEnum, metaclass=EarthingStickMeta):
    """
    Variable NodeID strings for all earthing stick statuses (read-only integer) and
    writable booleans for setting the earthing in manual mode.
    """

    status_1 = '"DB_Safety_Circuit"."Earthstick_1"."si_HMI_Status"'
    status_2 = '"DB_Safety_Circuit"."Earthstick_2"."si_HMI_Status"'
    status_3 = '"DB_Safety_Circuit"."Earthstick_3"."si_HMI_Status"'
    status_4 = '"DB_Safety_Circuit"."Earthstick_4"."si_HMI_Status"'
    status_5 = '"DB_Safety_Circuit"."Earthstick_5"."si_HMI_Status"'
    status_6 = '"DB_Safety_Circuit"."Earthstick_6"."si_HMI_Status"'

    manual_1 = '"DB_Safety_Circuit"."Earthstick_1"."sx_earthing_manually"'
    manual_2 = '"DB_Safety_Circuit"."Earthstick_2"."sx_earthing_manually"'
    manual_3 = '"DB_Safety_Circuit"."Earthstick_3"."sx_earthing_manually"'
    manual_4 = '"DB_Safety_Circuit"."Earthstick_4"."sx_earthing_manually"'
    manual_5 = '"DB_Safety_Circuit"."Earthstick_5"."sx_earthing_manually"'
    manual_6 = '"DB_Safety_Circuit"."Earthstick_6"."sx_earthing_manually"'

    operating_status_1 = '"DB_Safety_Circuit"."Earthstick_1"."sx_manual_control_active"'
    operating_status_2 = '"DB_Safety_Circuit"."Earthstick_2"."sx_manual_control_active"'
    operating_status_3 = '"DB_Safety_Circuit"."Earthstick_3"."sx_manual_control_active"'
    operating_status_4 = '"DB_Safety_Circuit"."Earthstick_4"."sx_manual_control_active"'
    operating_status_5 = '"DB_Safety_Circuit"."Earthstick_5"."sx_manual_control_active"'
    operating_status_6 = '"DB_Safety_Circuit"."Earthstick_6"."sx_manual_control_active"'

    @property
    def number(self) -> int:
        """
        Get corresponding earthing stick number.

        :return: earthing stick number (1..6)
        """
        return int(self.name.rpartition("_")[-1])

    @classmethod
    def range(cls) -> Sequence[int]:
        """
        Integer range of all earthing sticks.

        :return: sequence of earthing sticks numbers
        """
        return cls._range

    @classmethod
    def _validate_earthing_stick_number(cls, number: int):
        """
        Validate earthing stick number.

        :param number: the earthing stick number
        :raises ValueError: when earthing stick number is not valid
        """
        if number not in cls.range():
            raise ValueError(
                f"Earthing stick number must be one of {list(cls.range())}"
            )

    @classmethod
    def statuses(cls) -> Tuple["EarthingStick", ...]:
        """
        Get all earthing stick status instances.

        :return: tuple of status instances
        """
        return cls._statuses

    @classmethod
    def status(cls, number: int) -> "EarthingStick":
        """
        Get the status enum instance for an earthing stick number.

        :param number: the earthing stick (1..6)
        :return: the status instance
        :raises ValueError: when earthing stick number is not valid
        """
        cls._validate_earthing_stick_number(number)
        return cls.statuses()[number-1]

    @classmethod
    def manuals(cls) -> Tuple["EarthingStick", ...]:
        """
        Get all earthing stick manual instances.

        :return: tuple of manual instances
        """
        return cls._manuals

    @classmethod
    def manual(cls, number: int):
        """
        Get the manual enum instance for an earthing stick number.

        :param number: the earthing stick (1..6)
        :return: the manual instance
        :raises ValueError: when earthing stick number is not valid
        """
        cls._validate_earthing_stick_number(number)
        return cls.manuals()[number-1]

    @classmethod
    def operating_statuses(cls) -> Tuple["EarthingStick", ...]:
        """
        Get all earthing stick operating status instances.

        :return: tuple of operating status instances
        """
        return cls._operating_statuses

    @classmethod
    def operating_status(cls, number: int):
        """
        Get the operating status enum instance for an earthing stick number.

        :param number: the earthing stick (1..6)
        :return: the operating status instance
        :raises ValueError: when earthing stick number is not valid
        """
        cls._validate_earthing_stick_number(number)
        return cls.operating_statuses()[number-1]


@unique
class Errors(ValueEnum):
    """
    Variable NodeID strings for information regarding error, warning and message
    handling.
    """

    #: Boolean read-only variable telling if a message is active.
    message = '"DB_Message_Buffer"."Info_active"'

    #: Boolean read-only variable telling if a warning is active.
    warning = '"DB_Message_Buffer"."Warning_active"'

    #: Boolean read-only variable telling if a stop is active.
    stop = '"DB_Message_Buffer"."Stop_active"'

    #: Writable boolean for the error quit button.
    quit = '"DB_Message_Buffer"."Reset_button"'


class _AlarmEnumBase(_PrefixedNumbersEnumBase):
    """
    Base class for enums with "Alarm{n}" instance names, where n=1..N.
    """

    @classmethod
    def _prefix(cls) -> str:
        return "Alarm"

    @classmethod
    def Alarm(cls, number: int):
        """
        Get the enum instance for a given alarm number.

        :param number: the alarm number (1..N)
        :return: the enum instance for the alarm number.
        :raises ValueError: when alarm number is not in the 1..N range
        """
        return cls.get(number)


Alarms = unique(_AlarmEnumBase(
    "Alarms",
    {
        f"Alarm{n}":
            f'"DB_Alarm_HMI"."Alarm{n}"'
        for n in range(1, 152)
    },
))
"""
Alarms enumeration containing all variable NodeID strings for the alarm array.
"""


class DoorStatus(IntEnum):
    """
    Possible status values for doors.
    """

    #: not enabled in Supercube HMI setup, this door is not supervised.
    inactive = 0

    #: Door is open.
    open = 1

    #: Door is closed, but not locked.
    closed = 2

    #: Door is closed and locked (safe state).
    locked = 3

    #: Door has an error or was opened in locked state (either with emergency stop or
    #: from the inside).
    error = 4


class EarthingRodStatus(IntEnum):
    """
    Possible status values for earthing rods.
    """
    #: earthing rod is somewhere in the experiment
    #: and blocks the start of the experiment
    experiment_blocked = 0

    #: earthing rod is hanging next to the door, experiment is ready to operate
    experiment_ready = 1


class _DoorEnumBase(_PrefixedNumbersEnumBase):
    """
    Base class for enums with "status_{n}" instance names, where n=1..N is the door
    number.
    """

    @classmethod
    def _prefix(cls) -> str:
        return "status_"

    @classmethod
    def status(cls, door: int):
        """
        Get the enum instance for a given door number.

        :param number: the door number (1..N)
        :return: the enum instance for the given door number.
        :raises ValueError: when door number is not in the 1..N range
        """
        return cls.get(door)


Door = unique(_DoorEnumBase(
    "Door",
    {
        f"{_DoorEnumBase._prefix()}{n}":
            f'"DB_Safety_Circuit"."Door_{n}"."si_HMI_status"'
        for n in range(1, 4)
    }
))
"""
Variable NodeID strings for doors.
"""

EarthingRod = unique(_DoorEnumBase(
    "EarthingRod",
    {
        f"{_DoorEnumBase._prefix()}{n}":
            f'"DB_Safety_Circuit"."Door_{n}"."Ix_earthingrod"'
        for n in range(1, 4)
    }
))
"""
Variable NodeID strings for earthing rods.
"""


class AlarmText(ValueEnum):
    """
    This enumeration contains textual representations for all error classes (stop,
    warning and message) of the Supercube system. Use the :meth:`AlarmText.get`
    method to retrieve the enum of an alarm number.
    """

    # Safety elements
    Alarm1 = "STOP Emergency Stop 1"
    Alarm2 = "STOP Emergency Stop 2"
    Alarm3 = "STOP Emergency Stop 3"
    Alarm4 = "STOP Safety Switch 1 error"
    Alarm5 = "STOP Safety Switch 2 error"
    Alarm6 = "STOP Door 1 lock supervision"
    Alarm7 = "STOP Door 2 lock supervision"
    Alarm8 = "STOP Door 3 lock supervision"
    Alarm9 = "STOP Earthing stick 1 error while opening"
    Alarm10 = "STOP Earthing stick 2 error while opening"
    Alarm11 = "STOP Earthing stick 3 error while opening"
    Alarm12 = "STOP Earthing stick 4 error while opening"
    Alarm13 = "STOP Earthing stick 5 error while opening"
    Alarm14 = "STOP Earthing stick 6 error while opening"
    Alarm15 = "STOP Earthing stick 1 error while closing"
    Alarm16 = "STOP Earthing stick 2 error while closing"
    Alarm17 = "STOP Earthing stick 3 error while closing"
    Alarm18 = "STOP Earthing stick 4 error while closing"
    Alarm19 = "STOP Earthing stick 5 error while closing"
    Alarm20 = "STOP Earthing stick 6 error while closing"
    Alarm21 = "STOP Safety fence 1"
    Alarm22 = "STOP Safety fence 2"
    Alarm23 = "STOP OPC connection error"
    Alarm24 = "STOP Grid power failure"
    Alarm25 = "STOP UPS failure"
    Alarm26 = "STOP 24V PSU failure"

    # Doors
    Alarm41 = "WARNING Door 1: Use earthing rod!"
    Alarm42 = "MESSAGE Door 1: Earthing rod is still in setup."
    Alarm43 = "WARNING Door 2: Use earthing rod!"
    Alarm44 = "MESSAGE Door 2: Earthing rod is still in setup."
    Alarm45 = "WARNING Door 3: Use earthing rod!"
    Alarm46 = "MESSAGE Door 3: Earthing rod is still in setup."

    # General
    Alarm47 = "MESSAGE UPS charge < 85%"
    Alarm48 = "MESSAGE UPS running on battery"

    # generic not defined alarm text
    not_defined = "NO ALARM TEXT DEFINED"

    @classmethod
    def get(cls, alarm: int):
        """
        Get the attribute of this enum for an alarm number.

        :param alarm: the alarm number
        :return: the enum for the desired alarm number
        """

        try:
            return getattr(cls, "Alarm{}".format(alarm))
        except AttributeError:
            return cls.not_defined


class OpcControl(ValueEnum):
    """
    Variable NodeID strings for supervision of the OPC connection from the
    controlling workstation to the Supercube.
    """

    #: writable boolean to enable OPC remote control and display a message window on
    #: the Supercube HMI.
    active = '"DB_OPC_Connection"."sx_OPC_active"'
    live = '"DB_OPC_Connection"."sx_OPC_lifebit"'


class _LineEnumBase(_PrefixedNumbersEnumBase):
    """
    Base class for enums with "input_{n}" instance names, where n=1..N.
    """

    @classmethod
    def _prefix(cls) -> str:
        return "line_"

    @classmethod
    def line(cls, number: int):
        """
        Get the enum instance for a given line number.

        :param number: the line number (1..M)
        :return: the enum instance for the given line number.
        :raises ValueError: when line number is not in the 1..N range
        """
        return cls.get(number)


MessageBoard = unique(_LineEnumBase(
    "MessageBoard",
    {
        f"{_LineEnumBase._prefix()}{n}":
            f'"DB_OPC_Connection"."Is_status_Line_{n}"'
        for n in range(1, 16)
    }
))
"""
Variable NodeID strings for message board lines.
"""
