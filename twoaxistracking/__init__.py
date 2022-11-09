# Import of functions that should be accessible from the package top-level
from .layout import generate_field_layout  # noqa: F401
from .shading import shaded_fraction  # noqa: F401
from .trackerfield import TrackerField  # noqa: F401

try:
    from shapely.geos import lgeos  # noqa: F401
except OSError as err:  # pragma: no cover
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
