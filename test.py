"""A place for testing interactions in code"""
from urllib.request import *
from urllib.response import * 
from googleapiclient.discovery import build
from json import loads, dumps
from collections import namedtuple
import http.client
import os
import typing
import math

Coordinates = namedtuple("Coordinates", "longitude latitude")

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
    if not math.isclose(1.0, min_rating):
        ratingFilter["minRating"] = min_rating
    if not math.isclose(5.0, max_rating):
        ratingFilter["maxRating"] = max_rating
    if math.isclose(1.0, min_rating) and math.isclose(5.0, max_rating):
        return body
    
    add_filter(body, "ratingFilter", ratingFilter)
    return body

def filter_operating(body: dict) -> dict:
    operatingFilter = ["OPERATING_STATUS_OPERATIONAL"]
    add_filter(body, "operatingStatus", operatingFilter)
    return body

PRICE_RANGES = ["FREE", "INEXPENSIVE", "MODERATE", "EXPENSIVE", "VERY_EXPENSIVE"]
PRICE_FILTER_PREFIX = "PRICE_LEVEL_"
def filter_price(body: dict, min_price, max_price) -> dict:
    priceLevels = []
    for i in range(min_price, max_price):
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
EXCLUDE_PLACES = ["preschool", "primary_school", "secondary_school", "child_care_agency", "real_estate_agency", "corporate_office", "cemetary", "childrens_camp"]
def filter_place(body: dict, place) -> dict:
    pass

def get_weather():
    pass

# REST API formatting
test_data = {
  "insights": ["INSIGHT_PLACES", "INSIGHT_COUNT"],
  "filter": {
    "locationFilter": {
      "circle": {
        "radius" : 1609,
        "latLng": {"latitude": 33.6846, "longitude": -117.8265}
      }
    },
    "typeFilter": {
      "includedTypes": ["restaurant"]
    },
    "operatingStatus": ["OPERATING_STATUS_OPERATIONAL"],
    "priceLevels": [
      "PRICE_LEVEL_FREE",
      "PRICE_LEVEL_INEXPENSIVE"
    ],
    "ratingFilter": {
      "minRating": 4.0,
      "maxRating": 5.0
    }
  }
}

if __name__ == "__main__":
    request_data = {}
    irvine_coords = Coordinates(longitude=-117.8265, latitude=33.6846)
    insight_count(request_data)
    insight_locations(request_data)
    filter_radius(request_data, irvine_coords, 1609)
    filter_price(request_data, 0, 2)  # 1 + 1
    filter_rating(request_data, 2.5, 3.5)
    filter_operating(request_data)
    request_data["filter"]["typeFilter"] = {"includedTypes": ["restaurant"], "excludedTypes":[]}
    print(dumps(request_data, indent=4))
    with build("areainsights", "v1", developerKey=get_google_key()) as srvc:
        req = srvc.v1().computeInsights(body=request_data)
    print(dumps(req.execute(), indent=4))
# test = Request("https://areainsights.googleapis.com/v1:computeInsights", data=bytearray(str(test_data), "utf-8"), method="POST")
# test.add_header("X-Goog-Api-Key", get_google_key())
# test.add_header("Content-Type", "application/json")
# with urlopen(test) as response:
#     print(response.read().decode("utf-8"))
# from google_auth_oauthlib.flow import InstalledAppFlow

# compute flow
# area_srvc = build("areainsights", "v1", developerKey=get_google_key())  # use for getting locations
# area_rsrc = srvc.v1()  # to get computeInsights()  [why? ... Google]
# request = area_rsrc.computeInsights(body=data...)
# locations = loads(request.execute())
# --> {placeInsights: [{place:place_id}*]} -- place:place_id is in no particular order?
# if empty, returns empty dict

# --> get credentials for lifetime of program
# build places service
# get data for each location w/ place service
# !set header for each get request

# with build("areainsights", "v1", developerKey=get_google_key()) as service:
    # v1 = service.v1()
    # req = service.v1().computeInsights(body=test_data)
# v1.close()
# req = v1.computeInsights(body=test_data)  # this still works even if service.v1 is closed (explicitly)
# print(dumps(req.execute(), indent=2))

# flow = InstalledAppFlow.from_client_secrets_file("client_secrets_pls.json", ["https://www.googleapis.com/auth/cloud-platform"])
# credentials = flow.run_local_server(host='localhost',
#     port=8080, 
#     authorization_prompt_message='Please visit this URL: {url}', 
#     success_message='The auth flow is complete; you may close this window.',
#     open_browser=True)
# with build("places", "v1", developerKey=get_google_key()) as service:
#     places = service.places()
# req = places.get(name="places/ChIJvd0fPjrd3IARco_hP2Qga7c")
# # places.searchNearby()...
# # req.headers["X-Goog-FieldMask"] = "*"  # ",".join([])
# req.headers["X-Goog-FieldMask"] = "name,id,types,nationalPhoneNumber,formattedAddress,addressComponents,displayName,primaryTypeDisplayName,currentOpeningHours"
# print(req.execute())

# print(type(response))
# type(response).get(name="places/ChIJvd0fPjrd3IARco_hP2Qga7c")
# print(response.get("places/ChIJvd0fPjrd3IARco_hP2Qga7c"))
# print(response.read().decode("utf-8"))
# Google Locations

# curl --location 'https://areainsights.googleapis.com/v1:computeInsights' --header 'X-Goog-Api-Key: AIzaSyCi53EueOTCst5QXa6rawlV3r53QoZ4bRw' --header 'Content-Type: application/json' --data '{   "insights":[      "INSIGHT_COUNT"   ],   "filter":{      "locationFilter":{         "region":{            "place":"places/ChIJIQBpAG2ahYAR_6128GcTUEo"         }      },      "typeFilter":{         "includedTypes":[            "restaurant"         ]      },      "operatingStatus":[         "OPERATING_STATUS_OPERATIONAL"      ],      "priceLevels":[         "PRICE_LEVEL_INEXPENSIVE"      ],      "ratingFilter":{         "minRating":4.0,         "maxRating":5.0      }   }}'