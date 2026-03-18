from collections import namedtuple
from enum import Enum
import typing
import json

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
    # Measures time within a day in seconds; 0 - 24 * 3600
    def __init__(self, start, end):
        self.start, self.end = start, end

    def  __contains__(self, time):
        return self.start < time and self.end > time

    def __str__(self):
        return f"{self.start // 3600:>2}:{self.start % 3600:0<2} - {self.end // 3600:>2}:{self.end % 3600:0<2}"


class OpeningHours:
    # open times are listed, assume closed otherwise
    def __init__(self, open_times):
        def process_times(time_str):
            def time_to_int(time_str):
                clock_time, half = time_str.split(" ")
                time = 0
                if half == "pm":
                    time = 12 * 3600
                hours, minutes = clock_time.split(":")
                time += int(hours) * 3600 + int(minutes) * 60
                return time

            open_times = []
            if time_str == "closed":
                return open_times
            elif time_str == "open 24 hours":
                open_times.append(TimeInterval(0, 24 * 3600))
                return open_times
            for interval in time_str.split(", "):
                begin, end = interval.split(" – ")
                begin_time = time_to_int(begin)
                end_time = time_to_int(end)
                if "pm" in end and "am" not in begin:
                    begin_time += 12 * 3600
                open_times.append(TimeInterval(begin_time, end_time))
            return open_times
        
        # For use in time checking
        self.monday:    list[TimeInterval] = process_times(open_times[0])
        self.tuesday:   list[TimeInterval] = process_times(open_times[1])
        self.wednesday: list[TimeInterval] = process_times(open_times[2])
        self.thursday:  list[TimeInterval] = process_times(open_times[3])
        self.friday:    list[TimeInterval] = process_times(open_times[4])
        self.saturday:  list[TimeInterval] = process_times(open_times[5])
        self.sunday:    list[TimeInterval] = process_times(open_times[6])

        # For use in frontend
        self._monday:    str = open_times[0]
        self._tuesday:   str = open_times[1]
        self._wednesday: str = open_times[2]
        self._thursday:  str = open_times[3]
        self._friday:    str = open_times[4]
        self._saturday:  str = open_times[5]
        self._sunday:    str = open_times[6]

    def is_open(self, time: int, day: str):
        for interval in self.__getattribute__(day):
            if time in interval:
                return interval
        # return any((time in interval for interval in self.__getattribute__(day)))

    def to_json(self):
        return {
            "monday": self._monday,
            "tuesday": self._tuesday,
            "wednesday": self._wednesday,
            "thursday": self._thursday,
            "friday": self._friday,
            "saturday": self._saturday,
            "sunday": self._sunday,
        }
    

class Place:
    def __init__(self, place_data: tuple):
        self.id: str = place_data[0]
        self.display_name: str = place_data[1]
        self.pt_display: str = place_data[2]
        self.rating: float = place_data[3]
        self.primary_type: str = place_data[4]
        self.types: set[str] = set(place_data[5].split(","))
        self.price: Price = Price(place_data[6]) if place_data[6] else None
        self.address: str = place_data[7]
        self.coordinates: Coordinates = Coordinates(longitude=place_data[8], latitude=place_data[9])
        self.website: str = place_data[10]
        self.phone_number: str = place_data[11]

    def to_json(self):
        return self.id

    def __eq__(self, other):
        return type(other) is str and self.id == other or type(other) is Place and self.id == other.id

class UserModel:
    def __init__(self):
        self.id: str = ""
        self.saved: list[Place] = []
        self.preferred_types: set[str] = set()
        self.liked_places: list[Place] = []
        self.visited: list[Place] = []
    
    def add_visited(self, place):
        self.visited.append(place)

    def add_preferred_type(self, type):
        self.preferred_types.add(type)

    def add_liked_place(self, place):
        if place.id in (x.id for x in self.liked_places):
            return
        self.liked_places.append(place)

    def add_saved(self, place):
        if place.id in (x.id for x in self.saved):
            return
        self.saved.append(place)

    # def remove_visited(self, place_id):
    #     for i, place in enumerate(self.visited):
    #         if place.id == place_id:
    #             self.visited.pop(i)
    #             break
    def remove_visited(self, index):
        self.visited.pop(index)

    def remove_preferred_type(self, type):
        self.preferred_types.remove(type)

    def remove_liked_place(self, place_id):
        for i, place in enumerate(self.liked_places):
            if place.id == place_id:
                self.liked_places.pop(i)
                return
        raise KeyError(place_id)

    def remove_saved(self, place_id):
        for i, place in enumerate(self.saved):
            if place.id == place_id:
                self.saved.pop(i)
                return
        raise KeyError(place_id)
        
    def to_json(self) -> dict:
        user_obj = {"id": self.id,
                    "saved": [x.to_json() for x in self.saved],
                    "liked_places": [x.to_json() for x in self.liked_places],
                    "preferred_types": list(self.preferred_types),
                    "visited": [x.to_json() for x in self.visited],
        }
        return user_obj
