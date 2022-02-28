# Open source code for calculating self-shading of two-axis tracking solar collectors
"twoaxistracking" is a python package for simulating self-shading in fields of two-axis trackers.

## Documentation
The documentation can be found at [readthedocs](https://twoaxistracking.readthedocs.io/).

## Installation and dependencies
The package can be installed using pip:

    pip install twoaxistracking

The main non-standard dependency is `shapely`, which handles the geometric operations. It is recommended to install `shapely` using conda, which can be done by executing the following command in an Anaconda Prompt:

    conda install shapely

The solar modeling library `pvlib` is recommended for calculating the solar position and can be installed by the command:

## Citing
If you use the package in published work, please cite:
> Adam R. Jensen et al. 2022.
> "Self-shading of two-axis tracking solar collectors: Impact of field layout, latitude, and aperture shape."
> Accepted in Solar Energy.

## Contributing
Contributions to the repository, e.g., bug fixes and improvements to speed up the code are more than welcome.

## License
BSD 3-clause.
