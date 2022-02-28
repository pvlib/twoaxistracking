from twoaxistracking import shading, layout
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


def test_shading(rectangular_geometry, square_field_layout):
    # Test shading calculation
    # Also plots the geometry (ensures no errors occurs)
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    X, Y, Z, tracker_distance, relative_azimuth, relative_slope = \
        square_field_layout
    shaded_fraction = shading.shaded_fraction(
        solar_elevation=3,
        solar_azimuth=120,
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        min_tracker_spacing=min_tracker_spacing,
        tracker_distance=tracker_distance,
        relative_azimuth=relative_azimuth,
        relative_slope=relative_slope,
        slope_azimuth=0,
        slope_tilt=0,
        plot=True)
    assert np.isclose(shaded_fraction, 0.191324)


def test_shading_zero_solar_elevation(rectangular_geometry, square_field_layout):
    # Test shading when geometries completly overlap
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
    # Test shading calculation when there is no shading (high solar elevation)
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
