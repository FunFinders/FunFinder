from .data import *
from .database import get_place
from json import load, dump
import sqlite3

TEMP_TYPES = {'cafeteria', 'public_bathroom', 'bar', 'seafood_restaurant', 'sports_complex', 'grocery_store', 'dessert_shop', 'brazilian_restaurant', 'sushi_restaurant', 'sporting_goods_store', 'gas_station', 'health', 'juice_shop', 'deli', 'food_court', 'buffet_restaurant', 'food', 'barbecue_restaurant', 'french_restaurant', 'school', 'liquor_store', 'pizza_restaurant', 'japanese_restaurant', 'hamburger_restaurant', 'italian_restaurant', 'vegetarian_restaurant', 'bakery', 'night_club', 'turkish_restaurant', 'vegan_restaurant', 'restaurant', 'ice_cream_shop', 'video_arcade', 'mediterranean_restaurant', 'wine_bar', 'sports_club', 'finance', 'steak_house', 'asian_restaurant', 'bowling_alley', 'dessert_restaurant', 'breakfast_restaurant', 'food_delivery', 'internet_cafe', 'convenience_store', 'establishment', 'sports_coaching', 'sports_activity_location', 'store', 'swimming_pool', 'meal_takeaway', 'bagel_shop', 'pub', 'american_restaurant', 'catering_service', 'event_venue', 'food_store', 'mexican_restaurant', 'confectionery', 'meal_delivery', 'fast_food_restaurant', 'vietnamese_restaurant', 'indian_restaurant', 'bar_and_grill', 'thai_restaurant', 'acai_shop', 'middle_eastern_restaurant', 'candy_store', 'athletic_field', 'greek_restaurant', 'korean_restaurant', 'ramen_restaurant', 'chinese_restaurant', 'tea_house', 'fine_dining_restaurant', 'brunch_restaurant', 'atm', 'cafe', 'coffee_shop', 'sandwich_shop', 'wholesaler', 'donut_shop', 'golf_course', 'diner', 'point_of_interest'}


def get_user(user_filename, user: UserModel):
    conn = sqlite3.connect("places.db") 
    with open(user_filename) as file:
        user_json = load(file)
    user.id = user_json["id"]
    # should probably fetch them in one batch
    user.saved = [get_place(conn, id) for id in user_json["saved"]]
    user.preferred_types = set(user_json["preferred_types"])
    user.liked_places = [get_place(conn, id) for id in user_json["liked_places"]]
    user.visited = [get_place(conn, id) for id in user_json["visited"]]
    conn.close()
    return user

def store_user(user_filename, user: UserModel):
    with open(user_filename, 'w') as file:
        dump(user.to_json(), file, indent=2)

    # user_json = {
    #     "id": user.id,
    #     "saved": user.visited,
    #     "preferred_types": list(user.preferred_types),
    #     "liked_places": user.liked_places,
    #     "visited": user.visited
    # }

    # with open(user_filename, "w") as file:
    #     dump(user_json, file)
    # return user
