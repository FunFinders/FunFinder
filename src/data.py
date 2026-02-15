from collections import namedtuple
from enum import Enum
import typing

class Price(Enum):
    PRICE_LEVEL_FREE = 0
    PRICE_LEVEL_INEXPENSIVE = 1
    PRICE_LEVEL_MODERATE = 2
    PRICE_LEVEL_EXPENSIVE = 3
    PRICE_LEVEL_VERY_EXPENSIVE = 4

Coordinates = namedtuple("Coordinates", "latitude longitude")

class TimeInterval:
    # "open 24 hours" --> encompass entire time range
    # "closed" --> empty
    def __init__(self, start, end):
        self.start, self.end = start, end


class OpeningHours:
    # open times are listed, assume closed otherwise
    def __init__(self, open_times):
        def process_times(time_str):
            open_times = []
            for interval in time_str.split(", "):
                # process
                pass

        self.monday =    process_times(open_times[0])
        self.tuesday =   process_times(open_times[1])
        self.wednesday = process_times(open_times[2])
        self.thursday =  process_times(open_times[3])
        self.friday =    process_times(open_times[4])
        self.saturday =  process_times(open_times[5])
        self.sunday =    process_times(open_times[6])


class Place:
    def __init__(self, place_data: tuple):
        self.id = place_data[0]
        self.display_name = place_data[1]
        self.pt_display = place_data[2]
        self.rating = place_data[3]
        self.primary_type = place_data[4]
        self.types = set(place_data[5].split(","))
        self.price = place_data[6]
        self.address = place_data[7]
        self.coordinates: Coordinates = Coordinates(longitude=place_data[8], latitude=place_data[9])
        self.website = place_data[10]
        self.phone_number = place_data[11]


class UserModel:
    def __init__(self):
        self.id: str = ""
        self.saved: list[Place] = []
        self.preferred_types: set[str] = set()
        self.liked_places: list[Place] = []
        self.visited: list[Place] = []
