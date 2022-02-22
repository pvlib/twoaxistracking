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
        Collector geometry
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
    """

    def __init__(self, collector_geometry, neighbor_order, gcr,
                 aspect_ratio=None, offset=None, rotation=None,
                 layout_type=None):

        # Collector geometry
        self.collector_geometry = collector_geometry
        self.collector_area = self.collector_geometry.area
        self.L_min = layout._calculate_l_min(self.collector_geometry)
        # Field layout
        self.neighbor_order = neighbor_order
        self.gcr = gcr
        self.aspect_ratio = aspect_ratio
        self.offset = offset
        self.rotation = rotation
        # Calculate position of neighboring collectors based on field layout
        self.X, self.Y, self.tracker_distance, self.relative_azimuth = \
            layout.generate_field_layout(
                self.gcr, self.collector_area, self.L_min,
                neighbor_order=self.neighbor_order,
                aspect_ratio=self.aspect_ratio, offset=self.offset,
                rotation=self.rotation)
        plotting._plot_field_layout(X=self.X, Y=self.Y, L_min=self.L_min)

    def plot_field_layout(self):
        """Plot the field layout."""
        plotting._plot_field_layout(X=self.X, Y=self.Y, L_min=self.L_min)

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

        shaded_fractions = []
        for (elevation, azimuth) in zip(solar_elevation, solar_azimuth):
            shaded_fraction = shading.shaded_fraction(
                solar_elevation=elevation,
                solar_azimuth=azimuth,
                collector_geometry=self.collector_geometry,
                tracker_distance=self.tracker_distance,
                relative_azimuth=self.relative_azimuth,
                L_min=self.L_min,
                plot=False)
            shaded_fractions.append(shaded_fraction)

        # Return the shaded_fractions as the same type as the input
        if isinstance(solar_elevation, pd.Series):
            shaded_fractions = pd.Series(shaded_fractions,
                                         index=solar_elevation.index)
        elif isinstance(solar_elevation, np.array):
            shaded_fractions = np.array(shaded_fractions)

        return shaded_fractions
