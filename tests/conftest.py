import pytest
from shapely import geometry
import numpy as np
from twoaxistracking import layout


@pytest.fixture
def rectangular_geometry():
    collector_geometry = geometry.box(-2, -1, 2, 1)
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    return collector_geometry, min_tracker_spacing


@pytest.fixture
def circular_geometry():
    # A circular collector centered at (0,0) and has a radius of 2
    collector_geometry = geometry.Point(0, 0).buffer(2)
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    return collector_geometry, min_tracker_spacing


@pytest.fixture
def active_geometry_split():
    active_geometry_split = geometry.MultiPolygon([
        geometry.box(-1.9, -0.9, -0.1, -0.1),
        geometry.box(0.1, -0.9, 1.9, -0.1),
        geometry.box(-1.9, 0.1, -0.1, 0.9),
        geometry.box(0.1, 0.1, 1.9, 0.9)])
    return active_geometry_split


@pytest.fixture
def square_field_layout():
    # Corresponds to GCR 0.125 with the rectangular_geometry
    X = np.array([-8, 0, 8, -8, 8, -8, 0, 8])
    Y = np.array([-8, -8, -8, 0, 0, 8, 8, 8])
    tracker_distance = (X**2 + Y**2)**0.5
    relative_azimuth = np.array([225, 180, 135, 270, 90, 315, 0, 45])
    Z = np.zeros(8)
    relative_slope = np.zeros(8)
    return X, Y, Z, tracker_distance, relative_azimuth, relative_slope


@pytest.fixture
def square_field_layout_sloped(square_field_layout):
    # Corresponds to GCR 0.125 with the rectangular_geometry and tilted slope
    # Based on the square_field_layout
    X, Y, _, tracker_distance, relative_azimuth, _ = square_field_layout
    Z = np.array([0.12372765, 0.06186383, 0, 0.06186383,
                  -0.06186383, 0, -0.06186383, -0.12372765])
    relative_slope = np.array([5, 3.540025, 0, 3.540025,
                               -3.540025, 0, -3.540025, -5])
    return X, Y, Z, tracker_distance, relative_azimuth, relative_slope


def assert_isinstance(obj, klass):
    assert isinstance(obj, klass), f'got {type(obj)}, expected {klass}'
