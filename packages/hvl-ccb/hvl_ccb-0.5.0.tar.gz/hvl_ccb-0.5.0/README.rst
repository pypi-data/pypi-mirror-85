====================
HVL Common Code Base
====================

.. image:: https://gitlab.com/ethz_hvl/hvl_ccb/badges/master/pipeline.svg
        :target: https://gitlab.com/ethz_hvl/hvl_ccb/commits/master
        :alt: Pipeline status

.. image:: https://gitlab.com/ethz_hvl/hvl_ccb/badges/master/coverage.svg
        :target: https://gitlab.com/ethz_hvl/hvl_ccb/commits/master
        :alt: Coverage report

.. image:: https://readthedocs.org/projects/hvl-ccb/badge/?version=stable
        :target: https://hvl-ccb.readthedocs.io/en/latest/?badge=stable
        :alt: Documentation Status

Python common code base to control devices high voltage research devices, in
particular, as used in Christian Franck's High Voltage Lab (HVL), D-ITET, ETH.


* Free software: GNU General Public License v3
* Documentation:
    * if you're planning to develop start w/ reading "CONTRIBUTING.rst",
      otherwise either
    * read `HVL CCB documentation at RTD`_, or
    * install `Sphinx` and `sphinx_rtd_theme` Python packages and locally build docs
      on Windows in git-bash by running::

      $ ./make.sh docs

      from a shell with Make installed by running::

      $ make docs

      The target index HTML ("docs/_build/html/index.html") will open automatically in
      your Web browser.

.. _`HVL CCB documentation at RTD`: https://readthedocs.org/projects/hvl-ccb/


Features
--------

Manage experiments with :code:`ExperimentManager` instance controlling one or more of
the following devices:

* a MBW973 SF6 Analyzer / dew point mirror over a serial connection (COM-ports)
* a LabJack (T7-PRO) device using a LabJack LJM Library for communication
* a Schneider Electric ILS2T stepper motor drive over Modbus TCP
* a Elektro-Automatik PSI9000 DC power supply using VISA over TCP for communication
* a Rhode & Schwarz RTO 1024 oscilloscope using VISA interface over :code:`TCP::INSTR`
* a state-of-the-art HVL in-house Supercube device variants using an OPC UA client
* a Heinzinger Digital Interface I/II and a Heinzinger PNC power supply over a serial
  connection
* a passively Q-switched Pulsed Laser and a laser attenuator from CryLas over a serial
  connection
* a Newport SMC100PP single axis motion controller for 2-phase stepper motors over
  a serial connection
* a Pfeiffer TPG controller (TPG 25x, TPG 26x and TPG 36x) for Compact pressure Gauges
* a SST Luminox Oxygen sensor device controller over a serial connection
* a TiePie USB oscilloscope, generator and I2C host devices, as a wrapper of the Python
  bindings for the LibTiePie SDK
* a FuG Elektronik Power Supply (e.g. Capacitor Charger HCK) using the built-in ADDAT
  controller with the Probus V protocol over a serial connection



Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
