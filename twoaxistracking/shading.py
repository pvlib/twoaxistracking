import shapely
import numpy as np
from twoaxistracking import plotting


def _rotate_origin(x, y, rotation_deg):
    """Rotate a set of 2D points counterclockwise around the origin (0, 0)."""
    rotation_rad = np.deg2rad(rotation_deg)
    # Rotation is set negative to make counterclockwise rotation
    xx = x * np.cos(-rotation_rad) + y * np.sin(-rotation_rad)
    yy = -x * np.sin(-rotation_rad) + y * np.cos(-rotation_rad)
    return xx, yy


def shaded_fraction(solar_elevation, solar_azimuth, total_collector_geometry,
                    active_collector_geometry, L_min, tracker_distance,
                    relative_azimuth, plot=False):
    """Calculate the shaded fraction for any layout of two-axis tracking collectors.

    Parameters
    ----------
    solar_elevation: float
        Solar elevation angle in degrees.
    solar_azimuth: float
        Solar azimuth angle in degrees.
    total_collector_geometry: Shapely Polygon
        Polygon corresponding to the collector gross area.
    active_collector_geometry: Shapely Polygon or MultiPolygon
        One or more polygons defining the active collector area.
    L_min: float
        Minimum distance between collectors. Used for selecting possible
        shading collectors.
    tracker_distance: array of floats
        Distances between neighboring trackers and reference tracker.
    relative_azimuth: array of floats
        Relative azimuth between neigboring trackers and reference tracker.
    plot: bool, default: True
        Whether to plot the projected shadows and unshaded area.

    Returns
    -------
    shaded_fraction: float
        Shaded fraction for the specific solar position and field layout.
    """  # noqa: E501
    # If the sun is below the horizon, set the shaded fraction to nan
    if solar_elevation < 0:
        return np.nan

    azimuth_difference = solar_azimuth - relative_azimuth

    # Create mask to only calculate shading for collectors within +/-90° view
    mask = np.where(np.cos(np.deg2rad(azimuth_difference)) > 0)

    xoff = tracker_distance[mask]*np.sin(np.deg2rad(azimuth_difference[mask]))
    yoff = -tracker_distance[mask]\
        * np.cos(np.deg2rad(azimuth_difference[mask]))\
        * np.sin(np.deg2rad(solar_elevation))

    # Initialize the unshaded area as the collector aperture area
    unshaded_geometry = active_collector_geometry
    shading_geometries = []
    for i, (x, y) in enumerate(zip(xoff, yoff)):
        if np.sqrt(x**2+y**2) < L_min:
            # Project the geometry of the shading collector (gross area) onto
            # the plane of the investigated collector
            shading_geometry = shapely.affinity.translate(total_collector_geometry, x, y)  # noqa: E501
            # Update the unshaded area based on overlapping shade
            unshaded_geometry = unshaded_geometry.difference(shading_geometry)
            if plot:
                shading_geometries.append(shading_geometry)

    if plot:
        plotting._plot_shading(active_collector_geometry, unshaded_geometry,
                               shading_geometries, L_min)

    shaded_fraction = 1 - unshaded_geometry.area / active_collector_geometry.area
    return shaded_fraction
