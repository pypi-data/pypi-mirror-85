#!/usr/bin/env python
#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "pyserial>=3.4",
    "labjack-ljm>=1.20.0",
    "pymodbus>=2.3.0",
    "IPy>=0.83",
    "bitstring>=3.1.5",
    "pyvisa>=1.9.1",
    "pyvisa-py>=0.3.1",
    "typeguard>=2.3.0",
    "aenum>=2.1.2",
    "opcua>=0.98.6",
    "cryptography>=2.6.1",  # optional dependency of the opcua package
    "python-libtiepie>=0.7",
    "openpyxl>=2.6.2",
]

extra_requirements = {
    "numpy": ["numpy>=1.19.0"]
}


dependency_links = []

setup(
    author="Mikołaj Rybiński, David Graber, Henrik Menne, Alise Chachereau",
    author_email=(
        "mikolaj.rybinski@id.ethz.ch, dev@davidgraber.ch, henrik.menne@eeh.ee.ethz.ch, "
        "chachereau@eeh.ee.ethz.ch"
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=(
        "Python common code base to control devices high voltage research devices, in "
        "particular, as used in Christian Franck's High Voltage Lab (HVL), D-ITET, ETH"
    ),
    entry_points={},
    install_requires=requirements,
    extra_require=extra_requirements,
    dependency_links=dependency_links,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="hvl_ccb",
    name="hvl_ccb",
    package_data={"hvl_ccb": ["py.typed"], },
    packages=find_packages(),
    test_suite="tests",
    url="https://gitlab.com/ethz_hvl/hvl_ccb/",
    version='0.5.0',
    zip_safe=False,
)
