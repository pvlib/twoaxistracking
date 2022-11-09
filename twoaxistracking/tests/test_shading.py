from twoaxistracking import shading
import numpy as np


def test_shading(rectangular_geometry, active_geometry_split, square_field_layout):
    # Test shading calculation
    # Also plots the geometry (ensures no errors are raised)
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
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
