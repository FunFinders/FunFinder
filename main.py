import sqlite3
import time
import random
from googleapiclient.http import HttpError
from src.services import *
from src.data import Coordinates, Price
from src.database import *
from json import load, dumps

def tryExecute(request):
    try:
        return request.execute()
    except HttpError as error:
        print(f"{error.status_code}: {error.error_details}")
        return {"status": error.status_code, "details": error.error_details, "request_json": request.to_json()}

def add_opening_hours(database, times, place_id):
    if times is None or get_hours(database, place_id):
        return

    cursor = database.cursor()
    QUERY = """
        INSERT INTO OpeningHours (place_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday) 
        VALUES (:place_id, :monday, :tuesday, :wednesday, :thursday, :friday, :saturday, :sunday)
        """
    opening_hours = times.get("weekdayDescriptions")
    open_times = {}
    for hours in opening_hours:
        i = hours.split(": ")
        open_times[i[0].lower()] = i[1].strip().lower()
    open_times["place_id"] = place_id
    cursor.execute(QUERY, open_times)

def add_place(database, place_data):
    query = ""
    cursor = database.cursor()
    if not get_place(database, place_id):
        QUERY = """
        INSERT OR IGNORE INTO Places (place_id, display_name, primary_type_display_name, rating, primary_type, place_types, price, formatted_address, longitude, latitude, website, phone_number) 
        VALUES (:place_id, :display_name, :primary_type_display_name, :rating, :primary_type, :place_types, :price, :formatted_address, :longitude, :latitude, :website, :phone_number)
        """
    else:
        QUERY = """
        UPDATE Places
        SET place_id=:place_id, display_name=:display_name, primary_type_display_name=:primary_type_display_name, rating=:rating, primary_type=:primary_type, place_types=:place_types, price=:price, formatted_address=:formatted_address, longitude=:longitude, latitude=:latitude, website=:website, phone_number=:phone_number
        WHERE place_id=:place_id
    """
    place_id = place_data.get("id")
    display_name = place_data.get("displayName")
    if display_name:
        display_name = display_name["text"]
    ptdn = place_data.get("primaryTypeDisplayName")
    if ptdn:
        ptdn = ptdn["text"]
    primary_type = place_data.get("primaryType")
    types = ",".join(place_data.get("types"))
    rating = place_data.get("rating")
    price_str = place_data.get("priceLevel")
    price = None
    if price_str:
        price = Price[price_str].value
    formatted_address = place_data.get("formattedAddress")
    location = place_data.get("location")
    latitude = location["latitude"]
    longitude = location["longitude"]
    website = place_data.get("websiteUri")
    phoneNumber = place_data.get("nationalPhoneNumber")
    openingHours = place_data.get("regularOpeningHours")
    place_data = {
        "place_id": place_id,
        "display_name": display_name,
        "primary_type_display_name": ptdn,
        "rating": rating,
        "primary_type": primary_type,
        "place_types": types,
        "price": price,
        "formatted_address": formatted_address,
        "longitude": longitude,
        "latitude": latitude,
        "website": website,
        "phone_number": phoneNumber
    }
    cursor.execute(QUERY, place_data)
    add_opening_hours(database, openingHours, place_id)

def build_database():
    # sqlite3.connect("places.db")
    # request_data = {}
    # irvine_coords = Coordinates(longitude=-117.8265, latitude=33.6846)
    # insight_locations(request_data)
    # filter_radius(request_data, irvine_coords, 1609*2)
    # filter_operating(request_data)
    # filter_place(request_data, ["restaurant"])
    # for i in range(12, 52, 3):
    #     filter_rating(request_data, i/10 - .2, min(5, i/10))
    #     req = areaInsightsAPI.getInsights(body=request_data)
    #     results = tryExecute(req)
    #     print(dumps(results, indent=4))
    placeDB = sqlite3.connect("places.db")
    cursor = placeDB.cursor()
    cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS Places (
        place_id TEXT PRIMARY KEY,
        display_name TEXT,
        primary_type_display_name TEXT,
        rating REAL,
        primary_type TEXT,
        place_types TEXT,
        price INTEGER,
        formatted_address TEXT,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        website TEXT,
        phone_number TEXT
    );

    CREATE TABLE IF NOT EXISTS OpeningHours (
        place_id TEXT PRIMARY KEY, 
        monday TEXT,
        tuesday TEXT, 
        wednesday TEXT,
        thursday TEXT,
        friday TEXT,
        saturday TEXT,
        sunday TEXT,
        FOREIGN KEY (place_id) REFERENCES Places(place_id)
    );
    """
    )
    
    placeDB.commit()
    with open("out.txt") as file:
        obj = load(file)
    for place in obj["placeInsights"]:
        place_id = place["place"]
        data = tryExecute(placeAPI.getPlace(place_id))
        if random.random() > 0.8:
            print(dumps(data, indent=4))
        if type(data) is dict:
            add_place(placeDB, data)
        time.sleep(0.5)
    placeDB.commit()
    placeDB.close()


def main():
    build_database()


if __name__ == "__main__":
    main()
