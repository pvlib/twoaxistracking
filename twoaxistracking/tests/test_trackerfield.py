from twoaxistracking import trackerfield
import numpy as np
import pandas as pd
import pytest


def test_invalid_layout_type(rectangular_geometry):
    # Test if ValueError is raised when an incorrect layout_type is specified
    collector_geometry, min_tracker_spacing = rectangular_geometry
    with pytest.raises(ValueError, match="Layout type must be one of"):
        _ = trackerfield.TrackerField(
            total_collector_geometry=collector_geometry,
            active_collector_geometry=collector_geometry,
            neighbor_order=1,
            gcr=0.25,
            layout_type='this_is_not_a_layout_type')


def test_square_layout_type(rectangular_geometry):
    # Assert that layout field parameters are correctly set for the square layout
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
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
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
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
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
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
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
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
    collector_geometry, min_tracker_spacing = rectangular_geometry
    with pytest.raises(ValueError, match="needs to be specified"):
        _ = trackerfield.TrackerField(
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
    return [np.nan, 1.0, 0.7177496, 0.6036017, 0.0]


@pytest.fixture
def expected_datetime_index():
    return pd.date_range('2020-01-01 12', freq='15min', periods=5)


def test_calculation_of_shaded_fraction_list(rectangular_geometry, solar_position,
                                             expected_shaded_fraction):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are lists
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(solar_elevation, solar_azimuth)
    # Compare the calculated and expected shaded fraction
    np.testing.assert_allclose(result, expected_shaded_fraction)
    # Check that the output is of the same type as the inputs
    assert isinstance(result, list)


def test_calculation_of_shaded_fraction_series(
        rectangular_geometry, solar_position, expected_shaded_fraction, expected_datetime_index):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are pandas Series
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    # Set solar elevation and azimuth as pandas Series with datetime index
    solar_elevation, solar_azimuth = solar_position
    solar_elevation = pd.Series(solar_elevation)
    solar_azimuth = pd.Series(solar_azimuth)
    solar_elevation.index = expected_datetime_index
    solar_azimuth.index = expected_datetime_index
    result = field.get_shaded_fraction(solar_elevation, solar_azimuth)

    np.testing.assert_allclose(result, expected_shaded_fraction)
    assert isinstance(result, pd.Series)
    # Check that returned series of shaded fraction has correct index
    pd.testing.assert_index_equal(result.index, solar_elevation.index)


def test_calculation_of_shaded_fraction_array(rectangular_geometry, solar_position,
                                              expected_shaded_fraction):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are numpy arrays
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)
    solar_elevation, solar_azimuth = solar_position
    result = field.get_shaded_fraction(np.array(solar_elevation), np.array(solar_azimuth))

    np.testing.assert_allclose(result, expected_shaded_fraction)
    assert isinstance(result, np.ndarray)


def test_calculation_of_shaded_fraction_float(rectangular_geometry):
    # Test if shaded fraction is calculated correct when solar elevation and
    # azimuth are scalar
    # Also tests that no error is raised when total and active geometries are
    # identical.
    collector_geometry, min_tracker_spacing = rectangular_geometry
    field = trackerfield.TrackerField(
        total_collector_geometry=collector_geometry,
        active_collector_geometry=collector_geometry,
        neighbor_order=1,
        gcr=0.25,
        aspect_ratio=1,
        offset=0,
        rotation=170)

    result = field.get_shaded_fraction(40, 180)
    np.testing.assert_allclose(result, 0)
    assert np.isscalar(result)


def test_total_collector_geometry_encloses_active_areas(rectangular_geometry, circular_geometry):
    # Test that ValueError is raised if the aperture collector geometry is not
    # completely enclosed by the total collector geometry
    rectangular_collector, min_tracker_spacing = rectangular_geometry
    circular_collector, min_tracker_spacing = circular_geometry
    with pytest.raises(ValueError, match="does not completely enclose"):
        _ = trackerfield.TrackerField(
            total_collector_geometry=rectangular_collector,
            active_collector_geometry=circular_collector,
            neighbor_order=1,
            gcr=0.1,
            aspect_ratio=1,
            offset=0,
            rotation=0)
