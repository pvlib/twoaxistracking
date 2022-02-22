"""
The ``TwoAxisTrackerField`` module contains functions and classes that
combine the collector definition, field layout generation, and shading
calculation steps. Using the `TwoAxisTrackerField` class make it easy to
get started with the package and keeps track of the variables that are
passed from one function to the next.
"""

from twoaxistracking import layout, shading, plotting
import numpy as np
import pandas as pd


class TwoAxisTrackerField:
    """
    TwoAxisTrackerField is a convient container for the collector geometry
    and field layout, and allows for calculating the shaded fraction.

    Parameters
    ----------
    total_collector_geometry: Shapely Polygon
        Polygon corresponding to the total collector area.
    active_collector_geometry: Shapely Polygon or MultiPolygon
        One or more polygons defining the active collector area.
    neighbor_order: int
        Order of neighbors to include in layout. neighbor_order=1 includes only
        the 8 directly adjacent collectors.
    gcr: float
        Ground cover ratio. Ratio of collector area to ground area.
    aspect_ratio: float, optional
        Ratio of the spacing in the primary direction to the secondary.
    offset: float, optional
        Relative row offset in the secondary direction as fraction of the
        spacing in the secondary direction. -0.5 <= offset < 0.5.
    rotation: float, optional
        Counterclockwise rotation of the field in degrees. 0 <= rotation < 180
    layout_type: {square, square_rotated, hexagon_e_w, hexagon_n_s}, optional
        Specification of the special layout type (only depend on gcr).
    slope_azimuth : float, optional
        Direction of normal to slope on horizontal [degrees]
    slope_tilt : float, optional
        Tilt of slope relative to horizontal [degrees]
    """

    def __init__(self, total_collector_geometry, active_collector_geometry,
                 neighbor_order, gcr, aspect_ratio=None, offset=None,
                 rotation=None, layout_type=None, slope_azimuth=0,
                 slope_tilt=0):

        # Collector geometry
        self.total_collector_geometry = total_collector_geometry
        self.active_collector_geometry = active_collector_geometry
        # Derive properties from geometries
        self.total_collector_area = self.total_collector_geometry.area
        self.active_collector_area = self.active_collector_geometry.area
        self.L_min = layout._calculate_l_min(self.total_collector_geometry)

        # Field layout
        self.neighbor_order = neighbor_order
        self.gcr = gcr
        self.aspect_ratio = aspect_ratio
        self.offset = offset
        self.rotation = rotation
        self.layout_type = layout_type
        self.slope_azimuth = slope_azimuth
        self.slope_tilt = slope_tilt

        # Calculate position of neighboring collectors based on field layout
        self.X, self.Y, self.Z, self.tracker_distance, self.relative_azimuth, self.relative_slope = \
            layout.generate_field_layout(
                gcr=self.gcr, total_collector_area=self.total_collector_area,
                L_min=self.L_min, neighbor_order=self.neighbor_order,
                aspect_ratio=self.aspect_ratio, offset=self.offset,
                rotation=self.rotation, layout_type=self.layout_type,
                slope_azimuth=self.slope_azimuth, slope_tilt=self.slope_tilt,
                plot=False)

    def plot_field_layout(self):
        """Plot the field layout."""
        plotting._plot_field_layout(X=self.X, Y=self.Y, Z=self.Z,
                                    L_min=self.L_min)

    def get_shaded_fraction(self, solar_elevation,  solar_azimuth,
                            plot=False):
        """Calculate the shaded fraction for the specified solar positions.

        Uses the :py:func:`twoaxistracking.shaded_fraction` function to
        calculate the shaded fraction for to the specified solar elevation and
        azimuth angles.

        Parameters
        ----------
        solar_elevation : array-like
            Solar elevation angles in degrees.
        solar_azimuth : array-like
            Solar azimuth  angles in degrees.
        plot : boolean, default: False
            Whether to plot the unshaded and shading geometries for each solar
            position.

        Returns
        -------
        shaded_fractions : array-like
            The shaded fractions for the specified collector geometry,
            field layout, and solar angles.
        """
        # Wrap scalars in an array
        if isinstance(solar_elevation, (int, float)):
            solar_elevation = np.array([solar_elevation])
            solar_azimuth = np.array([solar_azimuth])

        # Calculate the shaded fraction for each solar position
        shaded_fractions = []
        for (elevation, azimuth) in zip(solar_elevation, solar_azimuth):
            shaded_fraction = shading.shaded_fraction(
                solar_elevation=elevation,
                solar_azimuth=azimuth,
                total_collector_geometry=self.total_collector_geometry,
                active_collector_geometry=self.active_collector_geometry,
                L_min=self.L_min,
                tracker_distance=self.tracker_distance,
                relative_azimuth=self.relative_azimuth,
                relative_slope=self.relative_slope,
                slope_azimuth=self.slope_azimuth,
                slope_tilt=self.slope_tilt,
                plot=False)
            shaded_fractions.append(shaded_fraction)

        # Return the shaded_fractions as the same type as the input
        if isinstance(solar_elevation, pd.Series):
            shaded_fractions = pd.Series(shaded_fractions,
                                         index=solar_elevation.index)
        elif isinstance(solar_elevation, np.array):
            shaded_fractions = np.array(shaded_fractions)

        return shaded_fractions
