from geopy.distance import geodesic, great_circle, Distance

from .location import Location


def great_circle_distance(l1: Location, l2: Location) -> Distance:
    loc1 = (l1.lat, l1.lng)
    loc2 = (l2.lat, l2.lng)
    return great_circle(loc1, loc2)


def geodesic_location_distance(l1: Location, l2: Location) -> Distance:
    """
    This uses a pure python library to compute distance between l1 and l2.
    """
    loc1 = (l1.lat, l1.lng)
    loc2 = (l2.lat, l2.lng)
    return geodesic(loc1, loc2)
