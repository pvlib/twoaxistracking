from twoaxistracking import shading
import numpy as np
from shapely import geometry
import shapely


def test_shading(rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shading calculation
    # Also plots the geometry (ensures no errors are raised)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=3,
        solar_azimuth=120,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=active_geometry_split,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=True)
    np.testing.assert_allclose(shaded_fraction, 0.190320666774)


def test_shading_zero_solar_elevation(rectangular_geometry, square_field_layout):
    # Test shading when geometries completely overlap
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=0,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=False)
    assert shaded_fraction == 1


def test_no_shading(rectangular_geometry, square_field_layout):
    # Test shading calculation when there is no shading (high solar elevation)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=45,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=False)
    assert shaded_fraction == 0


def test_shading_below_horizon(rectangular_geometry, square_field_layout):
    # Test shading calculation when sun is below the horizon (elevation<0)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=-5.1,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=False)
    assert np.isnan(shaded_fraction)


def test_shading_below_hill_horizon(rectangular_geometry, square_field_layout):
    # Test shading when sun is below horizon line caused by sloped surface
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=9,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=10,
        plot=False)
    assert shaded_fraction == 1


def test_shading_max_shading_elevation(rectangular_geometry, square_field_layout):
    # Test that shaded_fraction is set to one when the solar elevation angle
    # is greater than the max_shading_elevation (even though shading may occur)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=3,  # low solar elevation angle with guaranteed shading
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=10,
        max_shading_elevation=2,  # lower than true max angle for testing purposes
        plot=False)
    assert shaded_fraction == 0


def test_return_geometries_negative_solar_elevation(
        rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shaded_fraction function with return_geometries=True
    # for the conditions (solar_elevation < 0)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction, geometries = shading.shaded_fraction(
        solar_elevation=-10,  # Solar elevation less than 0
        solar_azimuth=120,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=active_geometry_split,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        # Also plots the geometry (ensures no errors are raised)
        plot=True,
        return_geometries=True)
    assert geometries['unshaded_geometry'].equals(geometry.Polygon())
    assert geometries['shading_geometries'] == []


def test_return_geometries_below_horizon(
        rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shaded_fraction function with return_geometries=True
    # for the cases when solar elevation is below horizon (sloped ground)
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction, geometries = shading.shaded_fraction(
        solar_elevation=1,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=active_geometry_split,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=5,
        plot=False,
        return_geometries=True)
    assert geometries['unshaded_geometry'].equals(geometry.Polygon())
    assert geometries['shading_geometries'] == []


def test_return_geometries_above_max_shading_elevation(
        rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shaded_fraction function with return_geometries=True
    # for the case when the solar elevation angle is greater than the
    # maximum_shading_elevation
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction, geometries = shading.shaded_fraction(
        solar_elevation=89,
        solar_azimuth=180,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=active_geometry_split,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        max_shading_elevation=50,  # force max_shading_elevation
        plot=False,
        return_geometries=True)
    assert geometries['unshaded_geometry'].equals(active_geometry_split)
    assert geometries['shading_geometries'] == []


def test_return_geometries_normal_case(
        rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shaded_fraction function with return_geometries=True
    # for the cases when there is partly overlap between shading geometries and
    # the active area
    collector_geometry, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    _, geometries = shading.shaded_fraction(
        solar_elevation=5.2,
        solar_azimuth=145,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=active_geometry_split,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=True,
        return_geometries=True)
    expected_active_geometry = geometry.MultiPolygon([
            geometry.box(-1.9, -0.9, -0.1, -0.1),
            # The shading areas overlap the bottom right panel of the collector
            #  geometry.box(0.1, -0.9, 1.9, -0.1),
            geometry.box(-1.9, 0.1, -0.1, 0.9),
            geometry.box(0.1, 0.1, 1.9, 0.9)])
    expected_shading_geometries = shapely.affinity.translate(
        collector_geometry, 1.9646048635, -1.0098126057)
    assert geometries['unshaded_geometry'].equals(expected_active_geometry)
    assert geometries['shading_geometries'][0].equals_exact(
        expected_shading_geometries, tolerance=0.00001)
    assert len(geometries['shading_geometries']) == 1
