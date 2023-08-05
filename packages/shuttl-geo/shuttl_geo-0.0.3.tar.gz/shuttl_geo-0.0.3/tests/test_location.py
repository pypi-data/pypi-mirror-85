import pytest

from shuttl_geo import Location, random_location


@pytest.mark.parametrize("lat,lng", [(90, 190), (90.1, 179), (90.1, 180.001)])
def test_location_constructer_disallows_lat_lng_values_which_are_out_of_range(
    lat: float, lng: float
):
    with pytest.raises(AssertionError):
        Location(lat, lng)


@pytest.mark.parametrize("lat,lng", [(90.0, 180.0), (-90.0, -180.0)])
def test_location_constructer_with_valid_values(lat: float, lng: float):
    loc = Location(lat, lng)
    assert lat == loc.lat
    assert lng == loc.lng


@pytest.mark.parametrize("lat,lng", [(90.0, 180.0), (-90.0, -180.0)])
def test_location_equality_hash(lat: float, lng: float):
    loc = Location(lat, lng)
    loc2 = Location(lat, lng)
    assert loc == loc2
    assert hash(loc) == hash(loc2)


# NOTE: This test just exists to verify if the method call succeeds or not
def test_random_location_works():
    random_location()
