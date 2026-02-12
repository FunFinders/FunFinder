"""A place for testing interactions in code"""
from urllib.request import *
from urllib.response import * 
from googleapiclient.discovery import build
from json import loads, dumps
from collections import namedtuple
import os
import typing
import math


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