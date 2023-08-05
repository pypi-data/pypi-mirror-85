from shuttl_geo import Location
from shuttl_geo.distance import geodesic_location_distance, great_circle_distance


def test_location_distance_to():
    l1 = Location(28.434816, 77.049327)
    l2 = Location(28.443195, 77.057225)

    assert 1208.6872544594537 == geodesic_location_distance(l1, l2).meters


def test_location_distance_to_fast():
    l1 = Location(28.434816, 77.049327)
    l2 = Location(28.443195, 77.057225)

    assert 1210.134381048365 == great_circle_distance(l1, l2).meters
