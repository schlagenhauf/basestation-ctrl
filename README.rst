..
  .. image:: https://api.cirrus-ci.com/github/schlagenhauf/basestation-ctrl.svg?branch=main
      :alt: Built Status
      :target: https://cirrus-ci.com/github/schlagenhauf/basestation-ctrl
  .. image:: https://readthedocs.org/projects/basestation-ctrl/badge/?version=latest
      :alt: ReadTheDocs
      :target: https://basestation-ctrl.readthedocs.io/en/stable/
  .. image:: https://img.shields.io/coveralls/github/schlagenhauf/basestation-ctrl/main.svg
      :alt: Coveralls
      :target: https://coveralls.io/r/schlagenhauf/basestation-ctrl
  .. image:: https://img.shields.io/pypi/v/basestation-ctrl.svg
      :alt: PyPI-Server
      :target: https://pypi.org/project/basestation-ctrl/
  .. image:: https://img.shields.io/conda/vn/conda-forge/basestation-ctrl.svg
      :alt: Conda-Forge
      :target: https://anaconda.org/conda-forge/basestation-ctrl
  .. image:: https://pepy.tech/badge/basestation-ctrl/month
      :alt: Monthly Downloads
      :target: https://pepy.tech/project/basestation-ctrl
  .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
      :alt: Twitter
      :target: https://twitter.com/basestation-ctrl
  .. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
      :alt: Project generated with PyScaffold
      :target: https://pyscaffold.org/

|

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

* Option B: ~Install from PyPI~ (coming soon)

Then consult
::

    basestation-ctrl --help

for details.

ToDos
=====
* Detect if Bluetooth is available and turned on
* Add commands for identifying the base stations and printing their status

Known Issues
============
* root (e.g. `sudo`) permissions are required for a scan. See: https://github.com/IanHarvey/bluepy/issues/313

About
=====

basestation-ctrl is based on `lh2ctrl <https://github.com/risa2000/lh2ctrl>`_
and `basestation <https://github.com/jariz/basestation>`_.