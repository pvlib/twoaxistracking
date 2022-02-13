# Shading of two-axis tracking collectors

"Two-axis tracker shading" is a python package for simulating self-shading in fields of two-axis trackers.

In the photovoltaics community, two-axis trackers are also commonly referred to as dual-axis trackers (DAT).

## Installation



The main non-standard dependency is `shapely`, which handles the geometric operations. It is recommended to install `shapely` using conda, which can be done by executing the following command in an Anaconda Prompt:

    conda install shapely

The solar modeling library `pvlib` is recommended for calculating the solar position and can similarly be installed by the command:

    conda install pvlib

## Contributing
Contributions to the repository, e.g., bug fixes and improvements to speed up the code are more than welcome.


## License
BSD 3-clause.

## Citing
If you use the package in published work, please cite:
> Adam R. Jensen, Ioannis Sifnaios, Simon Furbo, and Janne Dragsted.
> "Self-shading of two-axis tracking solar collectors: Impact of field layout, latitude, and aperture shape."
> Submitted to Solar Energy.


```{toctree}
:maxdepth: 1
:hidden:

notebooks/Example time series generation
documentation
whatsnew
notebooks/Barstow_data
notebooks/numerical_simulations
```
