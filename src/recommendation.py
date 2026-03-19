from .data import Place, UserModel, Coordinates
from math import log, tanh
from collections import defaultdict
import geopy.distance  # --> .kilometers; .km, .miles, .mi
import typing

WEIGHT_SUBTYPE = 4
WEIGHT_PRIMARY = 10

def weight_distance(place: Place, origin: Coordinates):
    # some inverse relation; closer is better; log rule for better smoothness
    # min 0, max 10
    if origin is None:  # can't weight
        return 0
    distance = geopy.distance.distance(place.coordinates, origin).km
    return 2 - (tanh(distance) + 1)  # some smoothing function

# like rank_visited, but for liked places
def rank_liked(place: Place, user: UserModel, location: Coordinates = None):
    type_occurs = defaultdict(int)
    total_types = 0
    for place in user.liked_places:
        total_types += len(place.types)
        for type in place.types:
            type_occurs[type] += 1
    for key, value in type_occurs.items():
        type_occurs[key] = value / total_types
    weight = 0
    for place_type in place.types:
        if place_type is place.primary_type and place_type in type_occurs:
            weight += WEIGHT_PRIMARY * type_occurs[place_type]
        elif place_type in type_occurs:
            weight += WEIGHT_SUBTYPE * type_occurs[place_type]
    return weight

# primary type gets the most weight, followed by other place types; averaged
# rating scales weight
# distance is added to final weight
def rank_rule(places: list[Place], user: UserModel, location: Coordinates = None):
    place_weights = []
    for place in places:
        weight = 0
        # add rating instead?
        if place.rating is not None:
            weight = log(place.rating + 1)  # product after the fact
        for type in user.preferred_types:
            if type == place.primary_type:
                weight += WEIGHT_PRIMARY / len(place.types)
                # norm by number of types in the place, more tags a place has may be more diluted?
                # weight += WEIGHT_SUBTYPE / (1 + len(user.preferred_types))  # little softer + average
            elif type in place.types:
                weight += WEIGHT_SUBTYPE / len(place.types)  # little softer + average
        weight += rank_liked(place, user, location)
        # weight *= scale
        weight += weight_distance(place, location)
        place_weights.append((weight, place))

    return place_weights

# count type of places visited in the last {min 10, max 20} places
# weighted average over place
# primary type gets boosted weight
# multiply by ranking, scaled by log
# add distance weight
# TODO: add preference weighting
def rank_history(places: list[Place], user: UserModel, location: Coordinates = None):
    total_types = 0
    type_occurs = defaultdict(int)
    i = 0
    for place in user.visited[::-1]:
        i += 1
        total_types += len(place.types)
        for type in place.types:
            type_occurs[type] += 1
        if i == 20:
            break
    for key, value in type_occurs.items():
        type_occurs[key] = value / total_types
    place_weights = []
    for place in places:
        weight = 0
        for type in place.types:
            val = type_occurs.get(type, 0) * WEIGHT_SUBTYPE
            if type is place.primary_type:
                val *= 2
            weight += val
        
        weight += rank_liked(place, user, location)
        if place.rating is not None:
            # weight *= log(place.rating + 1)  # product after the fact
            weight += log(place.rating + 1)  # product after the fact
        weight += weight_distance(place, location)
        place_weights.append((weight, place))

    return place_weights

def rank_places(places: list[Place], user: UserModel, location: Coordinates = None):
    if len(user.visited) < 10:
        return rank_rule(places, user, location)
    else:
        return rank_history(places, user, location)
