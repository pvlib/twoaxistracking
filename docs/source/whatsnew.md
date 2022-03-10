# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added automatic documentation using Sphinx and autosummary
- Added ``__init__.py`` file
- Documentation is now hosted at [readthedocs](https://twoaxistracking.readthedocs.io/)
- Tilted fields can now be simulated by specifyig the keywords ``slope_azimuth`` and
   ``slope_tilt`` (see PR#7).
- The code now is able to differentiate between the active area and total area (see PR#11).
- The class TrackerField has been added, which is now the recommended way for using
  the package and is sufficient for most use cases.

### Changed
- Divide code into modules: shading, plotting, and layout
- Changed the overall file structure to become a Python package
- Changed names of notebooks
- Change repository name from "two_axis_tracker_shading" to
  "twoaxistracking"
- Changed naming of ``L_min`` to ``min_tracker_spacing``
- Changed naming of ``collector_area`` to ``total_collector_area``
- The field layout parameters are now required when using the
  {py:func}`twoaxistracking.layout.generate_field_layout` function. The standard field layouts
  are only available through the `TrackerField` class.

### Testing
- Linting using flake8 was added in PR#11

## [0.1.0] - 2022-01-25
This was the first release, containing the main functions and notebooks.
