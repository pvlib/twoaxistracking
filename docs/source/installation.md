# Installation

The package can be installed from [PyPI](https://pypi.org/) with the following command:

    pip install twoaxistracking

The main non-standard dependency is `shapely`, which handles the geometric operations (i.e., shading calculations). It is highly recommended to install `shapely` using conda, which can be done by executing the following command in an Anaconda Prompt:

    conda install shapely

The solar energy modeling library `pvlib` is recommended for calculating the solar position and can be installed by the command:

    pip install pvlib
