from googleapiclient.discovery import build
from googleapiclient.http import HttpError
from src.data import Coordinates
import os
import math
import sqlite3

MILE = 1609  # in meters

def get_google_key():
    return os.getenv("GOOGLE_API_KEY")

def get_user_location():
    pass

def get_time():
    pass

# API Requests

# Building request body
def insight_count(body: dict = None) -> dict:
    if body != None:
        if "insights" not in body:
            body["insights"] = []
        body["insights"].append("INSIGHT_COUNT")
    else:
        body = {"insights": ["INSIGHT_COUNT"]}
    return body

def insight_locations(body: dict = None) -> dict:
    if body != None:
        if "insights" not in body:
            body["insights"] = []
        body["insights"].append("INSIGHT_PLACES")
    else:
        body = {"insights": ["INSIGHT_PLACES"]}
    return body

def add_filter(body: dict, key, value) -> dict:
    if "filter" in body:
        body["filter"][key] = value
    else:
        body["filter"] = {key: value}
    return body

def filter_radius(body: dict, location: Coordinates, radius: float) -> dict:
    # radius in meters, must be greater than 22.27; pi * rad * rad > 1556.86
    coords = {"latitude": location.latitude, "longitude": location.longitude}
    circle = {"radius": radius, "latLng": coords}
    filter = {"circle": circle}
    add_filter(body, "locationFilter", filter)
    return body

def filter_rating(body: dict, min_rating=1.0, max_rating=5.0) -> dict:
    ratingFilter = {}
    if min_rating > max_rating:  # if min > max for whatever reason, clamp max to min value
        max_rating = min_rating
    if min_rating < 1.0 or max_rating > 5.0:  # error
        raise ValueError("min_rating or max_rating out of bounds")
        # return body
    if math.isclose(1.0, min_rating) and math.isclose(5.0, max_rating):
        return body
    if not math.isclose(1.0, min_rating):
        ratingFilter["minRating"] = min_rating
    if not math.isclose(5.0, max_rating):
        ratingFilter["maxRating"] = max_rating
    
    add_filter(body, "ratingFilter", ratingFilter)
    return body

def filter_operating(body: dict) -> dict:
    operatingFilter = ["OPERATING_STATUS_OPERATIONAL"]
    add_filter(body, "operatingStatus", operatingFilter)
    return body

PRICE_RANGES = ["FREE", "INEXPENSIVE", "MODERATE", "EXPENSIVE", "VERY_EXPENSIVE"]
PRICE_FILTER_PREFIX = "PRICE_LEVEL_"
def filter_price(body: dict, min_price, max_price) -> dict:
    # Price levels are associated from 0-4 inclusive
    if min_price == 0 and max_price == 4:
        return body
    priceLevels = []
    for i in range(min_price, max_price + 1):
        priceLevels.append(PRICE_FILTER_PREFIX + PRICE_RANGES[i])
    add_filter(body, "priceLevels", priceLevels)
    return body

PLACE_TYPES = [
    "bar", 
    "restaurant", 
    "meal_takeaway", 
    "fast_food_restaurant", 
    "fine_dining_restaurant", 
    "historical_landmark", 
    "tourist_attraction", 
    "amusement_park", 
    "museum", 
    "park", 
    "monument", 
    "bakery", 
    "gift_shop", 
    "clothing_store", 
    "grocery_store", 
    "supermarket", 
    "shopping_mall", 
    "convenience_store", 
    "hiking_area", 
    "visitor_center", 
    "tourist_information_center", 
    ]
EXCLUDE_PLACES = ["preschool", "primary_school", "secondary_school", "child_care_agency", "real_estate_agency", "corporate_office", "cemetery", "childrens_camp"]
def filter_place(body: dict, includedPlaces: list[str]) -> dict:
    typeFilter = {"includedTypes": [place for place in includedPlaces if place not in EXCLUDE_PLACES],
                  "excludedTypes": EXCLUDE_PLACES}
    add_filter(body, "typeFilter", typeFilter)
    return body


class _AreaInsights:
    def __init__(self):
        self._srvc = build("areainsights", "v1", developerKey=get_google_key())
        self.api = self._srvc.v1()

    def __del__(self):
        self._srvc.close()
        self.api.close()
    
    def getInsights(self, body):
        return self.api.computeInsights(body=body)


class _Place:
    def __init__(self):
        self._srvc = build("places", "v1", developerKey=get_google_key())
        self.api = self._srvc.places()

    def __del__(self):
        self._srvc.close()
        self.api.close()

    def getPlace(self, placeId) -> dict:
        req = self.api.get(name=placeId)
        req.headers["X-Goog-FieldMask"] = "*"
        return req 
   

areaInsightsAPI = _AreaInsights()
placeAPI = _Place()

def tryExecute(request):
    try:
        return request.execute()
    except HttpError as error:
        print(f"{error.status_code}: {error.error_details}")
        return {"status": error.status_code, "details": error.error_details, "request_json": request.to_json()}


if __name__ == "__main__":
    from json import dumps, loads
    request_data = {}
    irvine_coords = Coordinates(longitude=-117.8265, latitude=33.6846)
    insight_count(request_data)
    insight_locations(request_data)
    filter_radius(request_data, irvine_coords, 1609)
    filter_price(request_data, 0, 1)
    filter_rating(request_data, 4.3, 4.6)
    # filter_rating(request_data, max_rating=1.1)

    filter_operating(request_data)
    filter_place(request_data, ["restaurant"])
    req = areaInsightsAPI.getInsights(request_data)
    # print(dumps(request_data, indent=4))

    # with build("areainsights", "v1", developerKey=get_google_key()) as srvc:
    #     req = srvc.v1().computeInsights(body=request_data)
    result = tryExecute(req)
    print(dumps(result, indent=4))
    place = result["placeInsights"][0]["place"]
    place_details = tryExecute(placeAPI.getPlace(place))
    print(dumps(place_details, indent=4))
    

__all__ = ["areaInsightsAPI", 
           "placeAPI", 
           "insight_count", 
           "insight_locations",
           "filter_radius",
           "filter_price",
           "filter_rating",
           "filter_operating",
           "filter_place",
           "get_user_location",
           "get_time",
           ]
