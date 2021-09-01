# Self-shading of two-axis tracking solar collectors
This repository contains functions for simulation shading in fields of two-axis solar trackers.

The two main functions are `generate_field_layout` and `two_axis_shading_fraction`. The function `generate_field_layout` calculates the collector locations for a user-defined regular field layout. For an introduction to regular field layouts and the defining parameters, please see the paper by [Cumpston and Pye (2014)](https://doi.org/10.1016/j.solener.2014.06.012).

The function `two_axis_shading_fraction` is used to calculate the shading fraction based on a specific field layout and solar position. Check out the [example tutorial](https://github.com/AdamRJensen/two_axis_tracker_shading/blob/main/notebooks/Example%20time%20series%20generation.ipynb) to get started! Alternatively, each function is documented according to numpydoc style guide.


## Dependencies
The main non-standard dependency is `shapely`, which handles the geometric operations. It is recommended install `shapely` with anaconda, which can be done by executing the following command in an AnacondaPrompt:

    conda install shapely

The solar modeling library `pvlib` is recommended for calculating the solar position and can similarly be installed by the command:

    conda install pvlib

## Contributing
Contributions to the repository, e.g., bug fixes and improvements to speed up the code are more than welcome.


## License
BSD 3-clause.
