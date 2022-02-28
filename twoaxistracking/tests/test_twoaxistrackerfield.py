from twoaxistracking import layout, twoaxistrackerfield
from shapely import geometry
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def rectangular_geometry():
    collector_geometry = geometry.box(-2, -1, 2, 1)
    total_collector_area = collector_geometry.area
    min_tracker_spacing = layout._calculate_min_tracker_spacing(collector_geometry)
    return collector_geometry, total_collector_area, min_tracker_spacing


def test_invalid_layout_type(rectangular_geometry):
    # Test if ValueError is raised when an incorrect layout_type is specified
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    with pytest.raises(ValueError, match="Layout type must be one of"):
        _ = twoaxistrackerfield.TwoAxisTrackerField(
            total_collector_geometry=collector_geometry,
            active_collector_geometry=collector_geometry,
            neighbor_order=1,
            gcr=0.25,
            layout_type='this_is_not_a_layout_type')


def test_square_layout_type(rectangular_geometry):
    # Assert that layout field parameters are correctly set for the square layout
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=2,
        gcr=0.25,
        layout_type='square')
    assert field.gcr == 0.25
    assert field.aspect_ratio == 1
    assert field.offset == 0
    assert field.rotation == 0


def test_diagonal_layout_type(rectangular_geometry):
    # Assert that layout field parameters are correctly set for the diagonal layout
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=2,
        gcr=0.1,
        layout_type='diagonal')
    assert field.gcr == 0.1
    assert field.aspect_ratio == 1
    assert field.offset == 0
    assert field.rotation == 45


def test_hexagonal_n_s_layout_type(rectangular_geometry):
    # Assert that layout field parameters are correctly set for the diagonal layout
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=4,
        gcr=0.4,
        layout_type='hexagonal_n_s')
    assert field.gcr == 0.4
    assert field.aspect_ratio == np.sqrt(3)/2
    assert field.offset == -0.5
    assert field.rotation == 0


def test_hexagonal_e_w_layout_type(rectangular_geometry):
    # Assert that layout field parameters are correctly set for the diagonal layout
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=4,
        gcr=0.4,
        layout_type='hexagonal_e_w')
    assert field.gcr == 0.4
    assert field.aspect_ratio == np.sqrt(3)/2
    assert field.offset == -0.5
    assert field.rotation == 90


def test_unspecifed_layout_type(rectangular_geometry):
    # Test if ValueError is raised when one or more layout parameters are unspecified
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    with pytest.raises(ValueError, match="needs to be specified"):
        _ = twoaxistrackerfield.TwoAxisTrackerField(
            total_collector_geometry=collector_geometry,
            active_collector_geometry=collector_geometry,
            neighbor_order=1,
            gcr=0.25,
            aspect_ratio=1,
            offset=0,
            # rotation unspecified
        )


@pytest.fixture
def solar_position():
    solar_elevation = [-1, 0, 1, 2, 40]
    solar_azimuth = [90, 100, 110, 120, 180]
    return solar_elevation, solar_azimuth


@pytest.fixture
def expected_shaded_fraction():
    return [np.nan, 1.0, 0.71775, 0.60360, 0.0]


def is_close_with_nans(test, expected):
    return (np.isclose(test, expected) | (np.isnan(test) &
            (np.isnan(test) == np.isnan(expected)))).all()


def test_calculation_of_shaded_fraction_list(rectangular_geometry, solar_position,
                                             expected_shaded_fraction):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are lists
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(solar_elevation, solar_azimuth)
    # Test that calculated shaded fraction are equal or both nan
    # using np.isclose(np.nan, np.nan) does not identify
    assert is_close_with_nans(result, expected_shaded_fraction)
    assert isinstance(result, list)


def test_calculation_of_shaded_fraction_series(rectangular_geometry, solar_position,
                                               expected_shaded_fraction):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are pandas Series
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(pd.Series(solar_elevation), pd.Series(solar_azimuth))
    # Test that calculated shaded fraction are equal or both nan
    # using np.isclose(np.nan, np.nan) does not identify
    assert is_close_with_nans(result, expected_shaded_fraction)
    assert isinstance(result, pd.Series)


def test_calculation_of_shaded_fraction_array(rectangular_geometry, solar_position,
                                              expected_shaded_fraction):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are pandas Series
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(np.array(solar_elevation), np.array(solar_azimuth))
    # Test that calculated shaded fraction are equal or both nan
    # using np.isclose(np.nan, np.nan) does not identify
    assert is_close_with_nans(result, expected_shaded_fraction)
    assert isinstance(result, np.ndarray)


def test_calculation_of_shaded_fraction_float(rectangular_geometry, solar_position):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are pandas Series
    collector_geometry, total_collector_area, min_tracker_spacing = rectangular_geometry
    field = twoaxistrackerfield.TwoAxisTrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(40, 180)
    # Test that calculated shaded fraction are equal or both nan
    # using np.isclose(np.nan, np.nan) does not identify
    assert result == 0
    assert isinstance(result, np.ndarray)
