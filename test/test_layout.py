from twoaxistracking import layout
from shapely import geometry
import numpy as np
import pytest


@pytest.fixture
def rectangular_geometry():
    collector_geometry = geometry.box(-2, -1, 2, 1)
    total_collector_area = collector_geometry.area
    l_min = layout._calculate_l_min(collector_geometry)
    return collector_geometry, total_collector_area, l_min


def test_l_min_rectangle(rectangular_geometry):
    # Test calculation of L_min for a rectangular collector
    l_min = layout._calculate_l_min(rectangular_geometry[0])
    assert l_min == np.sqrt(4**2+2**2)


def test_l_min_circle():
    # Test calculation of L_min for a circular collector with radius 1
    collector_geometry = geometry.Point(0, 0).buffer(1)
    l_min = layout._calculate_l_min(collector_geometry)
    assert l_min == 2


def test_l_min_circle_offcenter():
    # Test calculation of L_min for a circular collector with radius 1 rotating
    # off-center around the point (0, 1)
    collector_geometry = geometry.Point(0, 1).buffer(1)
    l_min = layout._calculate_l_min(collector_geometry)
    assert l_min == 4


def test_l_min_polygon():
    # Test calculation of L_min for a polygon
    collector_geometry = geometry.Polygon([(-1, -1), (3, 2), (4, 4), (1, 2), (-1, -1)])
    l_min = layout._calculate_l_min(collector_geometry)
    assert l_min == 2 * np.sqrt(4**2 + 4**2)


def test_square_layout_generation(rectangular_geometry):
    # Test square field layout defined using tje built-in layout types
    collector_geometry, total_collector_area, L_min = rectangular_geometry

    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, layout_type='square',
            slope_azimuth=0, slope_tilt=0, plot=False)
    assert np.isclose(X, np.array([-5.65685425, 0, 5.65685425, -5.65685425,
                                   5.65685425, -5.65685425, 0, 5.65685425])
                      ).all()


def test_layout_generation_value_error(rectangular_geometry):
    # Test if value errors are correctly raised
    collector_geometry, total_collector_area, L_min = rectangular_geometry

    # Test if ValueError is raised when an incorrect layout_type is specified
    with pytest.raises(ValueError, match="layout type specified was not recognized"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, layout_type='this_is_not_a_layout_type')

    # Test if ValueError is raised if too few layout parameters are specified
    with pytest.raises(ValueError, match="no layout type has not been selected"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=0)

    # Test if ValueError is raised if offset is out of range
    with pytest.raises(ValueError, match="offset is outside the valid range"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=0, offset=1.1, aspect_ratio=1)

    # Test if ValueError is raised if aspect ratio is too low
    with pytest.raises(ValueError, match="Aspect ratio is too low"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=0, offset=0, aspect_ratio=0.6)

    # Test if ValueError is raised if aspect ratio is too high
    with pytest.raises(ValueError, match="Aspect ratio is too high"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=0, offset=0, aspect_ratio=5)

    # Test if ValueError is raised if rotation is outside valid range
    with pytest.raises(ValueError, match="rotation is outside the valid range"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=190, offset=0, aspect_ratio=1.2)

    # Test if ValueError is raised if L_min is outside valid range
    with pytest.raises(ValueError, match="Lmin is not physically possible"):
        _ = layout.generate_field_layout(
            gcr=0.25, total_collector_area=total_collector_area, L_min=1,
            neighbor_order=1, rotation=90, offset=0, aspect_ratio=1.2)

    # Test if ValueError is raised if rotation is outside valid range
    with pytest.raises(ValueError, match="Maximum ground cover ratio exceded"):
        _ = layout.generate_field_layout(
            gcr=0.5, total_collector_area=total_collector_area, L_min=L_min,
            neighbor_order=1, rotation=0, offset=0, aspect_ratio=1)

# Test custom layout
# Test slope
# Test neighbor order

# Inputs (0, negative numbers)
# All types of inputs, e.g., scalars, numpy array and series, list
# Test coverage
