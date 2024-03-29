# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5]

### Changed
- ``twoaxistracking.__version__`` now correctly reports the version string instead
  of raising ``AttributeError`` (see PR#45).


## [0.2.4] - 2023-01-05

### Changed
- Removed Shapely instalation check and added specific import of the affinity module
  to avoid import errors when using Shapely 2.0 (see PR#40).

### Testing
- Add python 3.11 to test matrix (see PR#38).


## [0.2.3] - 2022-11-11
It is now possible to export the unshaded area for further analysis. A GIF was added to the
main landing page, and a reference to the MethodsX article was added.

### Changed
- Added ``return_geometries`` parameter to the {py:func}`twoaxistracking.shaded_fraction`.
  When ``return_geometries`` is True, the function returns both the shaded fraction and a dictionary
  with the geometries of the unshaded area and the shading areas (see PR#33).

### Added
- Reference to the published MethodsX article describing the package (see PR#31).


## [0.2.2] - 2022-09-14
This update includes a bug fix in the calculation of the maximum shading elevation
and addition of a section on validation to the documentation.

### Changed
- Fix bug in the calculation of the maximum shading elevation at high GCRs (see PR#28).

### Added
- Button on the documentation website linking to GitHub (see PR#27).
- Notebook on the validation of the annual shading fraction calculation (see PR#29).

### Requirements
- Increased version of myst-nb and sphinx-book-theme in the ``[doc]`` optional requirements
  for building the documentation (see PR#29).


## [0.2.1] - 2022-03-11
Add pandas as a required dependency and fix the workflow file responsible for
uploading the package to PyPI.

### Requirements
- Added pandas to the list of required dependencies


## [0.2.0] - 2022-03-11
The code in the second release is a complete restructure in order for the code to be 
made into a package and available on PyPI.

### Added
- Added automatic documentation using Sphinx and autosummary
- Added ``__init__.py`` file
- Documentation is now hosted at [readthedocs](https://twoaxistracking.readthedocs.io/)
- Tilted fields can now be simulated by specifyig the keywords ``slope_azimuth`` and
   ``slope_tilt`` (see PR#7).
- The code now is able to differentiate between the active area and total area (see PR#11).
- The class {py:class}`twoaxistracking.TrackerField` has been added, which is now the recommended way for using
  the package and is sufficient for most use cases.
- Added {py:func}`twoaxistracking.layout.max_shading_elevation` for calculating the
  maximum elevation for which shading can occur for a specific field layout and collector geoemtry.
- Added {py:func}`twoaxistracking.shading.horizon_elevation_angle` for calculating the
  horizon angle caused by having a sloped field.

### Changed
- Divide code into modules: shading, plotting, and layout
- Changed the overall file structure to become a Python package
- Changed names of notebooks
- Change repository name from "two_axis_tracker_shading" to
  "twoaxistracking"
- Changed naming of ``L_min`` to ``min_tracker_spacing``
- Changed naming of ``collector_area`` to ``total_collector_area``
- The field layout parameters are now required when using the
  {py:func}`twoaxistracking.generate_field_layout` function. The standard field layouts
  are only available through the {py:class}`twoaxistracking.TrackerField` class.

### Testing
- Linting using flake8 was added in PR#11
- Test coverage was added in PR#14 and PR#16


## [0.1.0] - 2022-01-25
This was the first release, containing the main functions and notebooks.
