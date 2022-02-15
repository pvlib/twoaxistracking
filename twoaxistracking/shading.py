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


def shaded_fraction(solar_azimuth, solar_elevation,
                    collector_geometry, L_min, tracker_distance,
                    relative_azimuth, plot=False):
    """Calculate the shaded fraction for any layout of two-axis tracking collectors.

    Parameters
    ----------
    solar_azimuth: float
        Solar azimuth angle in degrees.
    solar_elevation: float
        Solar elevation angle in degrees.
    collector_geometry: Shapely geometry object
        The collector aperture geometry.
    L_min: float
        Minimum distance between collectors. Used for selecting possible
        shading collectors.
    tracker_distance: array of floats
        Distances between neighboring trackers and reference tracker.
    relative_azimuth: array of floats
        Relative azimuth between neigboring trackers and reference tracker.
    plot: bool, default: True
        Whether to plot the projected shadows.

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

    # Initialize the unshaded area as the collector area
    unshaded_geomtry = collector_geometry
    shade_geometries = []
    for i, (x, y) in enumerate(zip(xoff, yoff)):
        if np.sqrt(x**2+y**2) < L_min:
            # Project the geometry of the shading collector onto the plane
            # of the investigated collector
            shade_geometry = shapely.affinity.translate(collector_geometry, x, y)  # noqa: E501
            # Update the unshaded area based on overlapping shade
            unshaded_geomtry = unshaded_geomtry.difference(shade_geometry)
            if plot:
                shade_geometries.append(shade_geometry)

    if plot:
        plotting._plot_shading(
            collector_geometry, unshaded_geomtry, shade_geometries)

    shaded_fraction = 1 - unshaded_geomtry.area / collector_geometry.area
    return shaded_fraction
