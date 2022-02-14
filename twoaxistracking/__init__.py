from .layout import generate_field_layout
from .shading import shading_fraction


try:
    from shapely.geos import lgeos
except OSError as err:
    msg = (
        "An error was encountered when importing the shapely package. "
        "This often happens when a binary dependency is missing because "
        "shapely was installed from PyPI using pip. Try reinstalling shapely "
        "using conda with `conda install -c conda-forge shapely`, or "
        "alternatively from Christoph Gohlke's website if you're on Windows: "
        "https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely"
     )
    err.strerror += "; " + msg
    raise err
