# Installation

The package can be installed from [PyPI](https://pypi.org/) with the following command:

    pip install twoaxistracking

The main non-standard dependency is [shapely](https://shapely.readthedocs.io/en/stable/) which handles the geometric operations (i.e., shading calculations). It is highly recommended to install shapely using conda, which can be done by executing the following command in an Anaconda Prompt:

    conda install shapely

The solar energy modeling library [pvlib](https://pvlib-python.readthedocs.io/en/stable/) is recommended for calculating the solar position and can be installed by the command:

    pip install pvlib
