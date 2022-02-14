# Shading of two-axis tracking collectors

"Two-axis tracker shading" is a python package for simulating self-shading in fields of two-axis trackers.

If you want to get a quick-start on how to use the function, check out the [intro tutorial](../notebooks/intro_tutorial) which demosntrated how to use the package using examples. Otherwise feel free to peruse the [documentation](../documentation).

Note, in the photovoltaics community, two-axis trackers are also commonly referred to as dual-axis trackers (DAT).

## Installation
The main non-standard dependency is `shapely`, which handles the geometric operations. It is recommended to install `shapely` using conda, which can be done by executing the following command in an Anaconda Prompt:

    conda install shapely

The solar modeling library `pvlib` is recommended for calculating the solar position and can be installed by the command:

    pip install pvlib

## Contributing
Contributions to the repository, e.g., bug fixes and improvements to speed up the code are more than welcome!


## License
[BSD 3-clause](https://github.com/AdamRJensen/two_axis_tracker_shading/blob/main/LICENSE).

## Citing
If you use the package in published work, please cite:
> Adam R. Jensen et al. 2022.
> "Self-shading of two-axis tracking solar collectors: Impact of field layout, latitude, and aperture shape."
> Accepted in Solar Energy.


```{toctree}
:maxdepth: 1
:hidden:

notebooks/intro_tutorial
documentation
whatsnew
notebooks/reference_dataset
notebooks/field_layout_discretization
```
