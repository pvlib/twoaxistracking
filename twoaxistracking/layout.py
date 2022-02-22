import numpy as np
from twoaxistracking import plotting
from shapely import geometry


def _rotate_origin(x, y, rotation_deg):
    """Rotate a set of 2D points counterclockwise around the origin (0, 0)."""
    rotation_rad = np.deg2rad(rotation_deg)
    # Rotation is set negative to make counterclockwise rotation
    xx = x * np.cos(-rotation_rad) + y * np.sin(-rotation_rad)
    yy = -x * np.sin(-rotation_rad) + y * np.cos(-rotation_rad)
    return xx, yy


def _calculate_l_min(collector_geometry):
    L_min = 2 * collector_geometry.hausdorff_distance(geometry.Point(0, 0))
    return L_min


def generate_field_layout(gcr, total_collector_area, L_min, neighbor_order,
                          aspect_ratio=None, offset=None, rotation=None,
                          layout_type=None, slope_azimuth=0,
                          slope_tilt=0, plot=False):
    """
    Generate a regularly-spaced collector field layout.

    Field layout parameters and limits are described in [1]_.

    Notes
    -----
    The field layout can be specified either by selecting a standard layout
    using the layout_type argument or by specifying the individual layout
    parameters aspect_ratio, offset, and rotation. For both cases the ground
    cover ratio (gcr) needs to be specified.

    Any length unit can be used as long as the usage is consistent with the
    collector geometry.

    Parameters
    ----------
    gcr: float
        Ground cover ratio. Ratio of collector area to ground area.
    total_collector_area: float
        Surface area of one collector.
    L_min: float
        Minimum distance between collectors.
    neighbor_order: int
        Order of neighbors to include in layout. neighbor_order=1 includes only
        the 8 directly adjacent collectors.
    aspect_ratio: float, optional
        Ratio of the spacing in the primary direction to the secondary.
    offset: float, optional
        Relative row offset in the secondary direction as fraction of the
        spacing in the primary direction. -0.5 <= offset < 0.5.
    rotation: float, optional
        Counterclockwise rotation of the field in degrees. 0 <= rotation < 180
    layout_type: {square, square_rotated, hexagon_e_w, hexagon_n_s}, optional
        Specification of the special layout type (only depend on gcr).
    slope_azimuth : float, optional
        Direction of normal to slope on horizontal [degrees]
    slope_tilt : float, optional
        Tilt of slope relative to horizontal [degrees]
    plot: bool, default: False
        Whether to plot the field layout.

    Returns
    -------
    X: array of floats
        Distance of neighboring trackers to the reference tracker in the east-
        west direction. East is positive.
    Y: array of floats
        Distance of neighboring trackers to the reference tracker in the north-
        south direction. North is positive.
    Z: array of floats
        Relative heights of neighboring trackers.
    tracker_distance: array of floats
        Distances between neighboring trackers and the reference tracker.
    relative_azimuth: array of floats
        Relative azimuth of neighboring trackers - measured clockwise from
        north [degrees].
    relative_slope: array of floats
        Slope between neighboring trackers and reference tracker. A positive
        slope means neighboring collector is higher than reference collector.

    References
    ----------
    .. [1] `Shading and land use in regularly-spaced sun-tracking collectors, Cumpston & Pye.
       <https://doi.org/10.1016/j.solener.2014.06.012>`_
    """
    # Consider special layouts which can be defined only by GCR
    if layout_type == 'square':
        aspect_ratio = 1
        offset = 0
        rotation = 0
    # Diagonal layout is the square layout rotated 45 degrees
    elif layout_type == 'diagonal':
        aspect_ratio = 1
        offset = 0
        rotation = 45
    # Hexagonal layouts are defined by aspect_ratio=0.866 and offset=-0.5
    elif layout_type == 'hexagonal_n_s':
        aspect_ratio = np.sqrt(3)/2
        offset = -0.5
        rotation = 0
    # The hexagonal E-W layout is the hexagonal N-S layout rotated 90 degrees
    elif layout_type == 'hexagonal_e_w':
        aspect_ratio = np.sqrt(3)/2
        offset = -0.5
        rotation = 90
    elif layout_type is not None:
        raise ValueError('The layout type specified was not recognized.')
    elif ((aspect_ratio is None) or (offset is None) or (rotation is None)):
        raise ValueError('Aspect ratio, offset, and rotation needs to be '
                         'specified when no layout type has not been selected')

    # Check parameters are within their ranges
    if aspect_ratio < np.sqrt(1-offset**2):
        raise ValueError('Aspect ratio is too low and not feasible')
    if aspect_ratio > total_collector_area/(gcr*L_min**2):
        raise ValueError('Apsect ratio is too high and not feasible')
    if (offset < -0.5) | (offset >= 0.5):
        raise ValueError('The specified offset is outside the valid range.')
    if (rotation < 0) | (rotation >= 180):
        raise ValueError('The specified rotation is outside the valid range.')
    # Check if mimimum and maximum ground cover ratios are exceded
    gcr_max = total_collector_area / (L_min**2 * np.sqrt(1-offset**2))
    if (gcr < 0) or (gcr > gcr_max):
        raise ValueError('Maximum ground cover ratio exceded.')
    # Check if Lmin is physically possible given the collector area.
    if (L_min < np.sqrt(4*total_collector_area/np.pi)):
        raise ValueError('Lmin is not physically possible.')

    N = 1 + 2 * neighbor_order  # Number of collectors along each side

    # Generation of X and Y arrays with coordinates
    X = np.tile(np.arange(int(-N/2), int(N/2)+1), N)
    Y = np.repeat(np.arange(int(-N/2), int(N/2)+1), N)
    # Remove reference collector point (origin)
    X = np.delete(X, int(N**2/2))
    Y = np.delete(Y, int(N**2/2))

    # Add offset and implement aspect ratio. Note that it is important to first
    # calculate offset as it relies on the original X array.
    Y = Y + offset*X
    X = X * aspect_ratio
    # Apply field rotation
    X, Y = _rotate_origin(X, Y, rotation)
    # Calculate relative tracker height based on surface slope
    Z = - X * np.sin(np.deg2rad(slope_azimuth)) * \
        np.tan(np.deg2rad(slope_tilt)) \
        - Y * np.cos(np.deg2rad(slope_azimuth)) * \
        np.tan(np.deg2rad(slope_tilt))
    # Calculate and apply the scaling factor based on GCR
    scaling = np.sqrt(total_collector_area / (gcr * aspect_ratio))
    X, Y = X*scaling, Y*scaling

    # Calculate distance and angle of shading trackers relative to the center
    tracker_distance = np.sqrt(X**2 + Y**2)
    # The relative azimuth is defined clockwise eastwards from north
    relative_azimuth = np.mod(450-np.rad2deg(np.arctan2(Y, X)), 360)
    # Relative slope of collectors
    # positive means collector is higher than reference collector
    relative_slope = -np.cos(np.deg2rad(slope_azimuth - relative_azimuth)) * slope_tilt  # noqa: E501

    # Visualize layout
    if plot:
        plotting._plot_field_layout(X, Y, Z, L_min)

    return X, Y, Z, tracker_distance, relative_azimuth, relative_slope
