from twoaxistracking import layout, twoaxistrackerfield
from shapely import geometry
import numpy as np
import pytest


@pytest.fixture
def rectangular_geometry():
    collector_geometry = geometry.box(-2, -1, 2, 1)
    total_collector_area = collector_geometry.area
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    return collector_geometry, total_collector_area, min_tracker_spacing


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


def test_min_tracker_spacing_rectangle(rectangular_geometry):
    # Test calculation of min_tracker_spacing for a rectangular collector
    min_tracker_spacing = layout._calculate_min_tracker_spacing(rectangular_geometry[0])
    assert min_tracker_spacing == np.sqrt(4**2+2**2)


def test_min_tracker_spacing_circle():
    # Test calculation of min_tracker_spacing for a circular collector with radius 1
    collector_geometry = geometry.Point(0, 0).buffer(1)
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    assert min_tracker_spacing == 2


def test_min_tracker_spacing_circle_offcenter():
    # Test calculation of min_tracker_spacing for a circular collector with radius 1 rotating
    # off-center around the point (0, 1)
    collector_geometry = geometry.Point(0, 1).buffer(1)
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    assert min_tracker_spacing == 4


def test_min_tracker_spacingpolygon():
    # Test calculation of min_tracker_spacing for a polygon
    collector_geometry = geometry.Polygon([(-1, -1), (3, 2), (4, 4), (1, 2), (-1, -1)])
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    assert min_tracker_spacing == 2 * np.sqrt(4**2 + 4**2)


def test_square_layout_generation(rectangular_geometry, square_field_layout):
    # Test that a square field layout is returned correctly
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    X_exp, Y_exp, Z_exp, tracker_distance_exp, relative_azimuth_exp, relative_slope_exp = \
        square_field_layout

    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        layout.generate_field_layout(
            gcr=0.125,
            total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing,
            neighbor_order=1,
            aspect_ratio=1,
            offset=0,
            rotation=0)
    assert (X == X_exp).all()
    assert (Y == Y_exp).all()
    assert (Z == Z_exp).all()
    assert (tracker_distance_exp == tracker_distance_exp).all()
    assert (relative_azimuth == relative_azimuth_exp).all()
    assert (relative_slope == relative_slope_exp).all()


def test_layout_generation_value_error(rectangular_geometry):
    # Test if value errors are correctly raised
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry

    # Test if ValueError is raised if offset is out of range
    with pytest.raises(ValueError, match="offset is outside the valid range"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=1, offset=1.1, rotation=0)

    # Test if ValueError is raised if aspect ratio is too low
    with pytest.raises(ValueError, match="Aspect ratio is too low"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=0.6, offset=0, rotation=0)

    # Test if ValueError is raised if aspect ratio is too high
    with pytest.raises(ValueError, match="Aspect ratio is too high"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=5, offset=0, rotation=0)

    # Test if ValueError is raised if rotation is greater than 180 degrees
    with pytest.raises(ValueError, match="rotation is outside the valid range"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=1.2, offset=0, rotation=190)

    # Test if ValueError is raised if rotation is less than 0
    with pytest.raises(ValueError, match="rotation is outside the valid range"):
        _ = layout.generate_field_layout(
            gcr=0.5, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=1, offset=0, rotation=-1)

    # Test if ValueError is raised if min_tracker_spacing is outside valid range
    with pytest.raises(ValueError, match="Lmin is not physically possible"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area,
            min_tracker_spacing=1, neighbor_order=1, aspect_ratio=1.2,
            offset=0, rotation=90)

    # Test if ValueError is raised if maximum ground cover ratio is exceeded
    with pytest.raises(ValueError, match="Maximum ground cover ratio exceded"):
        _ = layout.generate_field_layout(
            gcr=0.5, total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing, neighbor_order=1,
            aspect_ratio=1, offset=0, rotation=0)


def test_field_slope():
    assert True


def test_neighbor_order(rectangular_geometry):
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        layout.generate_field_layout(
            gcr=0.125,
            total_collector_area=total_collector_area,
            min_tracker_spacing=min_tracker_spacing,
            neighbor_order=3,
            aspect_ratio=1,
            offset=0,
            rotation=0)
    assert len(X) == (7*7-1)

# Test slope
# Test neighbor order

# Inputs (0, negative numbers)
# All types of inputs, e.g., scalars, numpy array and series, list
# Test coverage
