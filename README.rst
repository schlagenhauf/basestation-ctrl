

.. image:: https://img.shields.io/pypi/v/basestation-ctrl.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/basestation-ctrl/
.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/


================
basestation-ctrl
================


    basestation-ctrl - A python library and CLI to wake up / power down SteamVR (Lighthouse) Base Stations. It currently only works for base stations v2.


Are you annoyed by the constant high-pitch noise in your room? Have you unplugged your base
stations and after repowering they are not in sleep mode anymore? Are you using SteamVR in
Windows but want to control your base stations in Linux? Then you've come to the right place.

basestation-ctrl allows you to power down, wake up and scan for base stations.

Tested on Arch Linux (2021-11-20) with Python 3.9.7 and SteamVR Base Station 2.0.

Usage
=====
(Note: I recommend using pipx instead of pip)


* Option A: Clone this repo and install from there:
  ::

      git clone https://github.com/schlagenhauf/basestation-ctrl.git
      pip install --user <path_to_repo>

* Option B: Install from PyPI
  ::

      pip install --user basestation-ctrl

Then consult
::

    basestation-ctrl --help

for details.

Examples
--------

::

    $ sudo basestation-ctrl scan
    aa:bb:cc:dd:ee:ff 11:22:33:44:55:66
    $ basestation-ctrl wake aa:bb:cc:dd:ee:ff 11:22:33:44:55:66
    $ basestation-ctrl sleep aa:bb:cc:dd:ee:ff 11:22:33:44:55:66

ToDos
=====
* Detect if Bluetooth interface is available and turned on
* Add commands for identifying the base stations and printing their status

Known Issues
============
* root (e.g. `sudo`) permissions are required for a scan. See: https://github.com/IanHarvey/bluepy/issues/313
* Hickups when trying to connect too often

About
=====

basestation-ctrl is based on `lh2ctrl <https://github.com/risa2000/lh2ctrl>`_
and `basestation <https://github.com/jariz/basestation>`_.