"""A place for testing interactions in code"""
from urllib.request import *
from urllib.response import * 
from googleapiclient.discovery import build
import http.client
import os
import typing

def get_google_key():
    return os.getenv("GOOGLE_API_KEY")

def to_data(obj):
    return bytearray(str(obj), "utf-8")

def from_data(datarr: bytearray):
    return datarr.decode("utf-8")

# API Requests
def get_insight_count(location: str) -> http.client.HTTPResponse:
    pass

def get_insight_location(locations: list[str]) -> http.client.HTTPResponse:
    pass

def add_filter():
    pass

# X-Goog-Api-Key:AIzaSyCi53EueOTCst5QXa6rawlV3r53QoZ4bRw

# REST API formatting
test_data = {
  "insights": ["INSIGHT_PLACES"],
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
    # "operatingStatus": ["OPERATING_STATUS_OPERATIONAL"],
    # "priceLevels": [
    #   "PRICE_LEVEL_FREE",
    #   "PRICE_LEVEL_INEXPENSIVE"
    # ],
    "ratingFilter": {
      "minRating": 1.0,
      "maxRating": 1.1
    }
  }
}
# test = Request("https://areainsights.googleapis.com/v1:computeInsights", data=bytearray(str(test_data), "utf-8"), method="POST")
# test.add_header("X-Goog-Api-Key", get_google_key())
# test.add_header("Content-Type", "application/json")
# with urlopen(test) as response:
#     print(response.read().decode("utf-8"))
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file("client_secrets_pls.json", ["https://www.googleapis.com/auth/cloud-platform"])
credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)
with build("places", "v1", developerKey=get_google_key(), credentials=credentials) as service:
    places = service.places()
req = places.get(name="places/ChIJvd0fPjrd3IARco_hP2Qga7c")
req.headers["X-Goog-FieldMask"] = "*"
print(req.execute())

# print(type(response))
# type(response).get(name="places/ChIJvd0fPjrd3IARco_hP2Qga7c")
# print(response.get("places/ChIJvd0fPjrd3IARco_hP2Qga7c"))
# print(response.read().decode("utf-8"))
# Google Locations

# curl --location 'https://areainsights.googleapis.com/v1:computeInsights' --header 'X-Goog-Api-Key: AIzaSyCi53EueOTCst5QXa6rawlV3r53QoZ4bRw' --header 'Content-Type: application/json' --data '{   "insights":[      "INSIGHT_COUNT"   ],   "filter":{      "locationFilter":{         "region":{            "place":"places/ChIJIQBpAG2ahYAR_6128GcTUEo"         }      },      "typeFilter":{         "includedTypes":[            "restaurant"         ]      },      "operatingStatus":[         "OPERATING_STATUS_OPERATIONAL"      ],      "priceLevels":[         "PRICE_LEVEL_INEXPENSIVE"      ],      "ratingFilter":{         "minRating":4.0,         "maxRating":5.0      }   }}'