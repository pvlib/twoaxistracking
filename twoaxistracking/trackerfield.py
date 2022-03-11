"""
The `trackerfield` module contains functions and classes that
combine the collector definition, field layout generation, and shading
calculation steps. Using the `TrackerField` class make it easy to
get started with the package and keeps track of the variables that are
passed from one function to the next.
"""

from twoaxistracking import layout, shading, plotting
import numpy as np
import pandas as pd


STANDARD_FIELD_LAYOUT_PARAMETERS = {
    'square': {'aspect_ratio': 1, 'offset': 0, 'rotation': 0},
    # Diagonal layout is the square layout rotated 45 degrees
    'diagonal': {'aspect_ratio': 1, 'offset': 0, 'rotation': 45},
    # Hexagonal layouts are defined by aspect_ratio=0.866 and offset=-0.5
    'hexagonal_n_s': {'aspect_ratio': np.sqrt(3)/2, 'offset': -0.5, 'rotation': 0},
    # The hexagonal E-W layout is the hexagonal N-S layout rotated 90 degrees
    'hexagonal_e_w': {'aspect_ratio': np.sqrt(3)/2, 'offset': -0.5, 'rotation': 90},
}


class TrackerField:
    """
    TrackerField is a convenient container for the collector geometry
    and field layout, and allows for calculating the shaded fraction.

    Parameters
    ----------
    total_collector_geometry: :py:class:`Shapely Polygon <Polygon>`
        Polygon corresponding to the total collector area.
    active_collector_geometry: :py:class:`Shapely Polygon <Polygon>` or :py:class:`MultiPolygon`
        One or more polygons defining the active collector area.
    neighbor_order: int
        Order of neighbors to include in layout. It is recommended to use a
        neighbor order of two.
    gcr: float
        Ground cover ratio. Ratio of collector area to ground area.
    layout_type: {square, square_rotated, hexagon_e_w, hexagon_n_s}, optional
        Specification of the special layout type (only depends on gcr).
    aspect_ratio: float, optional
        Ratio of the spacing in the primary direction to the secondary.
    offset: float, optional
        Relative row offset in the secondary direction as fraction of the
        spacing in the secondary direction. -0.5 <= offset < 0.5.
    rotation: float, optional
        Counterclockwise rotation of the field in degrees. 0 <= rotation < 180
    slope_azimuth : float, default : 0
        Direction of normal to slope on horizontal [degrees]
    slope_tilt : float, default : 0
        Tilt of slope relative to horizontal [degrees]

    Notes
    -----
    The field layout can be specified either by selecting a standard layout
    using the ``layout_type`` argument or by specifying the individual layout
    parameters ``aspect_ratio``, ``offset``, and ``rotation``. For both cases
    the ground cover ratio (``gcr``) needs to be specified.
    """

    def __init__(self, total_collector_geometry, active_collector_geometry,
                 neighbor_order, gcr, layout_type=None, aspect_ratio=None,
                 offset=None, rotation=None, slope_azimuth=0, slope_tilt=0):

        # Collector geometry
        self.total_collector_geometry = total_collector_geometry
        self.active_collector_geometry = active_collector_geometry
        # Derive properties from geometries
        self.total_collector_area = self.total_collector_geometry.area
        self.active_collector_area = self.active_collector_geometry.area
        self.min_tracker_spacing = \
            layout._calculate_min_tracker_spacing(self.total_collector_geometry)

        # Ensure that the total collector area contains the active areas
        if self.total_collector_geometry.contains(self.active_collector_geometry) is False:
            raise ValueError('The total collector geometry does not completely'
                             ' enclose the active collector geometry.')

        # Standard layout parameters
        if layout_type is not None:
            if layout_type not in list(STANDARD_FIELD_LAYOUT_PARAMETERS):
                raise ValueError('Layout type must be one of: '
                                 f'{list(STANDARD_FIELD_LAYOUT_PARAMETERS)}')
            else:
                layout_params = STANDARD_FIELD_LAYOUT_PARAMETERS[layout_type]
                aspect_ratio = layout_params['aspect_ratio']
                offset = layout_params['offset']
                rotation = layout_params['rotation']
        elif ((aspect_ratio is None) or (offset is None) or (rotation is None)):
            raise ValueError('Aspect ratio, offset, and rotation needs to be '
                             'specified when no layout type has been selected')

        # Field layout parameters
        self.neighbor_order = neighbor_order
        self.gcr = gcr
        self.layout_type = layout_type
        self.aspect_ratio = aspect_ratio
        self.offset = offset
        self.rotation = rotation
        self.slope_azimuth = slope_azimuth
        self.slope_tilt = slope_tilt

        # Calculate position of neighboring collectors based on field layout
        (self.X, self.Y, self.Z, self.tracker_distance, self.relative_azimuth,
         self.relative_slope) = \
            layout.generate_field_layout(
                gcr=self.gcr,
                total_collector_area=self.total_collector_area,
                min_tracker_spacing=self.min_tracker_spacing,
                neighbor_order=self.neighbor_order,
                aspect_ratio=self.aspect_ratio,
                offset=self.offset,
                rotation=self.rotation,
                slope_azimuth=self.slope_azimuth,
                slope_tilt=self.slope_tilt)

        # Calculate the maximum elevation angle for which shading can occcur
        self.max_shading_elevation = layout.max_shading_elevation(
            self.total_collector_geometry, self.tracker_distance, self.relative_slope)

    def plot_field_layout(self):
        """Create a plot of the field layout.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure with two axes
        """
        return plotting._plot_field_layout(
            X=self.X, Y=self.Y, Z=self.Z, min_tracker_spacing=self.min_tracker_spacing)

    def get_shaded_fraction(self, solar_elevation,  solar_azimuth,
                            plot=False):
        """Calculate the shaded fraction for the specified solar positions.

        Uses the :py:func:`twoaxistracking.shaded_fraction` function to
        calculate the shaded fraction for the specified solar elevation and
        azimuth angles.

        Parameters
        ----------
        solar_elevation : array-like
            Solar elevation angles in degrees.
        solar_azimuth : array-like
            Solar azimuth angles in degrees.
        plot : boolean, default: False
            Whether to plot the unshaded and shading geometries for each solar
            position.

        Returns
        -------
        shaded_fractions : array-like
            The shaded fractions for the specified collector geometry,
            field layout, and solar angles.
        """
        is_scalar = False
        # Wrap scalars in a list
        if np.isscalar(solar_elevation):
            solar_elevation = [solar_elevation]
            solar_azimuth = [solar_azimuth]
            is_scalar = True

        # Calculate the shaded fraction for each solar position
        shaded_fractions = []
        for (elevation, azimuth) in zip(solar_elevation, solar_azimuth):
            shaded_fraction = shading.shaded_fraction(
                solar_elevation=elevation,
                solar_azimuth=azimuth,
                total_collector_geometry=self.total_collector_geometry,
                active_collector_geometry=self.active_collector_geometry,
                min_tracker_spacing=self.min_tracker_spacing,
                tracker_distance=self.tracker_distance,
                relative_azimuth=self.relative_azimuth,
                relative_slope=self.relative_slope,
                slope_azimuth=self.slope_azimuth,
                slope_tilt=self.slope_tilt,
                max_shading_elevation=self.max_shading_elevation,
                plot=plot)
            shaded_fractions.append(shaded_fraction)

        # Return the shaded_fractions as the same type as the input
        if isinstance(solar_elevation, pd.Series):
            shaded_fractions = pd.Series(shaded_fractions,
                                         index=solar_elevation.index)
        elif isinstance(solar_elevation, np.ndarray):
            shaded_fractions = np.array(shaded_fractions)
        elif is_scalar:
            shaded_fractions = shaded_fractions[0]

        return shaded_fractions
