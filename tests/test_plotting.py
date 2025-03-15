import matplotlib.pyplot as plt
from twoaxistracking import plotting, trackerfield
from .conftest import assert_isinstance
import numpy as np
from shapely import geometry


def test_field_layout_plot():
    X = np.array([-8, 0, 8, -8, 8, -8, 0, 8])
    Y = np.array([-8, -8, -8, 0, 0, 8, 8, 8])
    Z = np.array([0.1237, 0.0619, 0, 0.0619, -0.0619, 0, -0.0619, -0.1237])
    L_min = 4.4721
    result = plotting._plot_field_layout(X, Y, Z, L_min)
    assert_isinstance(result, plt.Figure)
    plt.close('all')


def test_shading_plot(rectangular_geometry, active_geometry_split):
    collector_geometry, min_tracker_spacing = rectangular_geometry
    result = plotting._plot_shading(
        active_geometry_split,
        collector_geometry,
        collector_geometry,
        min_tracker_spacing)
    assert_isinstance(result, plt.Figure)
    plt.close('all')


def test_shading_plot_empty_active_area(rectangular_geometry, active_geometry_split):
    # This test serves to test the correct operation of the
    # _polygons_to_patch_collection function when the area of the Polygon is 0
    collector_geometry, min_tracker_spacing = rectangular_geometry
    result = plotting._plot_shading(
        geometry.Polygon(),
        collector_geometry,
        collector_geometry,
        min_tracker_spacing)
    assert_isinstance(result, plt.Figure)
    plt.close('all')


def test_plotting_of_field_layout(rectangular_geometry):
    # Test if plot_field_layout returns a figure object
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0.45,
        rotation=30,
    )
    result = field.plot_field_layout()
    assert_isinstance(result, plt.Figure)
    plt.close('all')
