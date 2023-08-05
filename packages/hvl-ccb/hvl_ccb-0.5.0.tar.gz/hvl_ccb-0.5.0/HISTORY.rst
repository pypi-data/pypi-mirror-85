=======
History
=======

0.5.0 (2020-11-11)
------------------

* TiePie USB oscilloscope, generator and I2C host devices, as a wrapper of the Python
  bindings for the LibTiePie SDK.
* a FuG Elektronik Power Supply (e.g. Capacitor Charger HCK) using the built-in ADDAT
  controller with the Probus V protocol over a serial connection
* All devices poling status or measurements use now a :code:`dev.utils.Poller` utility
  class.
* Extensions and improvements in existing devices:
    * In :code:`dev.rs_rto1024.RTO1024`: added Channel state, scale, range,
      position and offset accessors, and measurements activation and read methods.
    * In :code:`dev.sst_luminox.Luminox`: added querying for all measurements
      in polling mode, and made output mode activation more robust.
    * In :code:`dev.newport.NewportSMC100PP`: an error-prone
      :code:`wait_until_move_finished` method of replaced by a fixed waiting time,
      device operations are now robust to a power supply cut, and device restart is not
      required to apply a start configuration.
* Other minor improvements:
    * Single failure-safe starting and stopping of devices sequenced via
      :code:`dev.base.DeviceSequenceMixin`.
    * Moved :code:`read_text_nonempty` up to :code:`comm.serial.SerialCommunication`.
    * Added development Dockerfile.
    * Updated package and development dependencies: :code:`pymodbus`,
      :code:`pytest-mock`.

0.4.0 (2020-07-16)
------------------

* Significantly improved new Supercube device controller:
    - more robust error-handling,
    - status polling with generic :code:`Poller` helper,
    - messages and status boards.
    - tested with a physical device,
* Improved OPC UA client wrapper, with better error handling, incl. re-tries on
  :code:`concurrent.futures.TimeoutError`.
* SST Luminox Oxygen sensor device controller.
* Backward-incompatible changes:
    - :code:`CommunicationProtocol.access_lock` has changed type from
      :code:`threading.Lock` to :code:`threading.RLock`.
    - :code:`ILS2T.relative_step` and :code:`ILS2T.absolute_position` are now called,
      respectively, :code:`ILS2T.write_relative_step` and
      :code:`ILS2T.write_absolute_position`.
* Minor bugfixes and improvements:
    - fix use of max resolution in :code:`Labjack.set_ain_resolution()`,
    - resolve ILS2T devices relative and absolute position setters race condition,
    - added acoustic horn function in the 2015 Supercube.
* Toolchain changes:
    - add Python 3.8 support,
    - drop pytest-runner support,
    - ensure compatibility with :code:`labjack_ljm` 2019 version library.

0.3.5 (2020-02-18)
------------------

* Fix issue with reading integers from LabJack LJM Library (device's product ID, serial
  number etc.)
* Fix development requirements specification (tox version).

0.3.4 (2019-12-20)
------------------

* New devices using serial connection:
    * Heinzinger Digital Interface I/II and a Heinzinger PNC power supply
    * Q-switched Pulsed Laser and a laser attenuator from CryLas
    * Newport SMC100PP single axis motion controller for 2-phase stepper motors
    * Pfeiffer TPG controller (TPG 25x, TPG 26x and TPG 36x) for Compact pressure Gauges
* PEP 561 compatibility and related corrections for static type checking (now in CI)
* Refactorings:
    * Protected non-thread safe read and write in communication protocols
    * Device sequence mixin: start/stop, add/rm and lookup
    * `.format()` to f-strings
    * more enumerations and a quite some improvements of existing code
* Improved error docstrings (:code:`:raises:` annotations) and extended tests for
  errors.

0.3.3 (2019-05-08)
------------------

* Use PyPI labjack-ljm (no external dependencies)


0.3.2 (2019-05-08)
------------------

* INSTALLATION.rst with LJMPython prerequisite info


0.3.1 (2019-05-02)
------------------

* readthedocs.org support

0.3 (2019-05-02)
----------------

* Prevent an automatic close of VISA connection when not used.
* Rhode & Schwarz RTO 1024 oscilloscope using VISA interface over TCP::INSTR.
* Extended tests incl. messages sent to devices.
* Added Supercube device using an OPC UA client
* Added Supercube 2015 device using an OPC UA client (for interfacing with old system
  version)

0.2.1 (2019-04-01)
------------------

* Fix issue with LJMPython not being installed automatically with setuptools.

0.2.0 (2019-03-31)
------------------

* LabJack LJM Library communication wrapper and LabJack device.
* Modbus TCP communication protocol.
* Schneider Electric ILS2T stepper motor drive device.
* Elektro-Automatik PSI9000 current source device and VISA communication wrapper.
* Separate configuration classes for communication protocols and devices.
* Simple experiment manager class.

0.1.0 (2019-02-06)
------------------

* Communication protocol base and serial communication implementation.
* Device base and MBW973 implementation.
