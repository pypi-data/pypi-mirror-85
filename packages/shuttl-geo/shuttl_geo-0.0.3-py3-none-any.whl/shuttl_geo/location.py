from dataclasses import dataclass

from shapely.geometry import Point
import random


@dataclass(frozen=True)
class Location:
    lat: float
    lng: float

    def __post_init__(self):
        assert -90 <= self.lat <= 90
        assert -180 <= self.lng <= 180

    def as_point(self) -> Point:
        return Point(self.lng, self.lat)


def random_location() -> Location:
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    return Location(lat, lng)
