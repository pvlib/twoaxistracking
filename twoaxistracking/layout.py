import numpy as np
from shapely import geometry


def _rotate_origin(x, y, rotation_deg):
    """Rotate a set of 2D points counterclockwise around the origin (0, 0)."""
    rotation_rad = np.deg2rad(rotation_deg)
    # Rotation is set negative to make counterclockwise rotation
    xx = x * np.cos(-rotation_rad) + y * np.sin(-rotation_rad)
    yy = -x * np.sin(-rotation_rad) + y * np.cos(-rotation_rad)
    return xx, yy


def _calculate_min_tracker_spacing(collector_geometry):
    min_tracker_spacing = 2 * collector_geometry.hausdorff_distance(geometry.Point(0, 0))
    return min_tracker_spacing


def generate_field_layout(gcr, total_collector_area, min_tracker_spacing,
                          neighbor_order, aspect_ratio, offset, rotation,
                          slope_azimuth=0, slope_tilt=0):
    """
    Generate a regularly-spaced collector field layout.

    Field layout parameters and limits are described in [1]_.

    Any length unit can be used as long as the usage is consistent with the
    collector geometry.

    Parameters
    ----------
    gcr: float
        Ground cover ratio. Ratio of collector area to ground area.
    total_collector_area: float
        Surface area of one collector.
    min_tracker_spacing: float
        Minimum distance between collectors.
    neighbor_order: int
        Order of neighbors to include in layout. It is recommended to use a
        neighbor order of 2.
    aspect_ratio: float
        Ratio of the spacing in the primary direction to the secondary.
    offset: float
        Relative row offset in the secondary direction as fraction of the
        spacing in the primary direction. -0.5 <= offset < 0.5.
    rotation: float
        Counterclockwise rotation of the field in degrees. 0 <= rotation < 180
    slope_azimuth : float, optional
        Direction of normal to slope on horizontal [degrees]
    slope_tilt : float, optional
        Tilt of slope relative to horizontal [degrees]

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
    # Check parameters are within their ranges
    if (offset < -0.5) | (offset >= 0.5):
        raise ValueError('The specified offset is outside the valid range.')
    if (rotation < 0) | (rotation >= 180):
        raise ValueError('The specified rotation is outside the valid range.')
    # Check if Lmin is physically possible given the collector area.
    if (min_tracker_spacing < np.sqrt(4*total_collector_area/np.pi)):
        raise ValueError('Lmin is not physically possible.')
    # Check if mimimum and maximum ground cover ratios are exceded
    gcr_max = total_collector_area / (min_tracker_spacing**2 * np.sqrt(1-offset**2))
    if (gcr < 0) or (gcr > gcr_max):
        raise ValueError('Maximum ground cover ratio exceded or less than 0.')
    if aspect_ratio < np.sqrt(1-offset**2):
        raise ValueError('Aspect ratio is too low and not feasible')
    if aspect_ratio > total_collector_area/(gcr*min_tracker_spacing**2):
        raise ValueError('Aspect ratio is too high and not feasible')

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
    relative_slope = np.rad2deg(np.arctan(-np.cos(np.deg2rad(slope_azimuth - relative_azimuth))
                                          * np.tan(np.deg2rad(slope_tilt))))

    return X, Y, Z, tracker_distance, relative_azimuth, relative_slope


def max_shading_elevation(total_collector_geometry, tracker_distance,
                          relative_slope):
    """Calculate the maximum elevation angle for which shading can occur.

    Parameters
    ----------
    total_collector_geometry: :py:class:`Shapely Polygon <Polygon>`
        Polygon corresponding to the total collector area.
    tracker_distance: array-like
        Distances between neighboring trackers and the reference tracker.
    relative_slope: array-like
        Slope between neighboring trackers and reference tracker. A positive
        slope means neighboring collector is higher than reference collector.

    Returns
    -------
    max_shading_elevation: float
        The highest solar elevation angle for which shading can occur for a
        given field layout and collector geometry [degrees]

    Note
    ----
    The maximum shading elevation angle is calculated for all neighboring
    trackers using the bounding box geometry and the bounding circle. For
    rectangular collectors (as approximated when using the bounding box), the
    maximum shading elevation occurs when one of the upper corners of the
    projected shading geometry and the lower corner of the reference collector
    intersects. For circular collectors (as approximated by the bounding
    cirlce), the maximum elevation occurs when the projected shadow is directly
    below the reference collector and the two circles tangent to each other.

    The maximum elevation is calculated using both the bounding box and the
    bounding circle, and the minimum of these two elevations is returned. For
    rectangular and circular collectors, the maximum elevation is exact,
    whereas for other geometries, the returned elevation is a conservative
    estimate.
    """
    # Calculate extent of box bounding the total collector geometry
    x_min, y_min, x_max, y_max = total_collector_geometry.bounds
    # Collector dimensions
    x_dim = x_max - x_min
    y_dim = y_max - y_min
    delta_gamma_rad = np.arcsin(x_dim / tracker_distance)
    # Calculate max elevation based on the bounding box (rectangular)
    max_elevations_rectangular = np.rad2deg(np.arcsin(
        y_dim * np.cos(np.deg2rad(relative_slope)) /
        (tracker_distance * np.cos(delta_gamma_rad)))) + relative_slope
    # Calculate max elevations using the minimum bounding diameter (circular)
    D_min = _calculate_min_tracker_spacing(total_collector_geometry)
    max_elevations_circular = np.rad2deg(np.arcsin(
        (D_min * np.cos(np.deg2rad(relative_slope)))/tracker_distance)) \
        + relative_slope
    # Compute max elevation
    max_elevation = np.nanmin([np.nanmax(max_elevations_rectangular),
                               np.nanmax(max_elevations_circular)])
    return max_elevation
