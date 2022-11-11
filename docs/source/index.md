# Simulating two-axis tracking solar collectors

`twoaxistracking` is a python package for simulating two-axis tracking solar collectors, particularly self-shading.

For a quick introduction to the package, check out the [intro tutorial](../notebooks/intro_tutorial) which demonstrates the main functionality. For further details, check out the [code documentation](../documentation).

An example of how shading varies over the course of one day for a hexagonal layout is shown below:

![gif demonstrating shading during one day](/shading_demonstration.gif)

Note, in the photovoltaics community, two-axis trackers are also commonly referred to as dual-axis trackers (DAT).


## Limitations
The package has been designed primarily with concentrating technologies in mind. As these technologies rely on an optical concentrator, they require accurate tracking (e.g., backtracking is not an option).
The underlying methodology, therefore, assumes that the reference collector and its neighbors are always oriented normal to the sun; hence, there is no way to provide an actual tracker position that differs from the solar position.
Additionally, the calculation of the shaded fraction only considers direct normal irradiance (DNI), as diffuse irradiance cannot be concentrated.


## Contributing
Contributions to the repository, e.g., bug fixes, feature request are more than welcome!


## License
[BSD 3-clause](https://github.com/pvlib/twoaxistracking/blob/main/LICENSE).


## Citing
If you use the package in published work, please cite:
> Adam R. Jensen, Ioannis Sifnaios, and Kevin Anderson. "twoaxistracking – a python package for simulating
> self-shading of two-axis tracking solar collectors." MethodsX, 9, 101876, (2022).
> [https://doi.org/10.1016/j.mex.2022.101876](https://doi.org/10.1016/j.mex.2022.101876)

and

> Adam R. Jensen, Ioannis Sifnaios, Simon Furbo, and Janne Dragsted. "Self-shading of two-axis
> tracking solar collectors: Impact of field layout, latitude, and aperture shape." Solar
> Energy, 236, 215–224, (2022). [https://doi.org/10.1016/j.solener.2022.02.023](https://doi.org/10.1016/j.solener.2022.02.023)


```{toctree}
:maxdepth: 1
:hidden:

notebooks/intro_tutorial
installation
documentation
whatsnew
notebooks/reference_dataset
notebooks/validation
notebooks/field_layout_discretization
```
