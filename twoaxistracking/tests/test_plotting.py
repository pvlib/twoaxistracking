import matplotlib.pyplot as plt
from twoaxistracking import plotting, layout, twoaxistrackerfield
from shapely import geometry
import numpy as np
import pytest


def assert_isinstance(obj, klass):
    assert isinstance(obj, klass), f'got {type(obj)}, expected {klass}'


def test_field_layout_plot():
    X = np.array([-8, 0, 8, -8, 8, -8, 0, 8])
    Y = np.array([-8, -8, -8, 0, 0, 8, 8, 8])
    Z = np.array([0.1237, 0.0619, 0, 0.0619, -0.0619, 0, -0.0619, -0.1237])
    L_min = 4.4721
    result = plotting._plot_field_layout(X, Y, Z, L_min)
    assert_isinstance(result, plt.Figure)
    plt.close('all')


@pytest.fixture
def rectangular_geometry():
    collector_geometry = geometry.box(-2, -1, 2, 1)
    total_collector_area = collector_geometry.area
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    return collector_geometry, total_collector_area, min_tracker_spacing


def test_shading_plot(rectangular_geometry):
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    result = plotting._plot_shading(collector_geometry, collector_geometry,
                                    collector_geometry, min_tracker_spacing)
    assert_isinstance(result, plt.Figure)
    plt.close('all')


def test_plotting_of_field_layout(rectangular_geometry):
    # Test if plot_field_layout returns a figure object
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
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
