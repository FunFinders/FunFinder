from flask import Flask, jsonify, request
from flask_cors import CORS  # Add this import
from src.data import UserModel, Place
from src.recommendation import rank_places
from src.user import get_user, store_user
from time import time
import src.database
import sqlite3

# use jsonify
# make_response ... .set_cookie(key, value)?
# request.cookies?
ACTIVE_USERS = {}

def _load_user(id="123"):
    user = UserModel()
    return get_user("user.json", user)

def _get_user(id="123"):
    if id in ACTIVE_USERS:
        return ACTIVE_USERS[id]
    else:
        try:
            user = _load_user()
        except:
            user = create_user()
        ACTIVE_USERS[user.id] = user
        return user

def _get_query() -> list[str]:
    args = request.args
    arguments = []
    min_rating = float(args.get("min_rating", 1.0))
    max_rating = float(args.get("max_rating", 5.0))

    rating_filter = src.database.filter_rating(min_rating, max_rating)

    min_price = int(args.get("min_price", 0))
    max_price = int(args.get("max_price", 4))

    price_filter = src.database.filter_price(min_price, max_price)

    tags = args.get("tags", "")
    tag_filter = ""
    if tags:
        tag_list = tags.split(",")
        tag_filter = src.database.filter_type_disjunctive(tag_list)

    search = args.get("name", "")
    if search:
        search_filter = src.database.filter_name()
        arguments.append(search)
    else:
        search_filter = ""

    filters = [rating_filter, price_filter, tag_filter, search_filter]
    # return filters
    return filters, arguments


app = Flask(__name__)
CORS(app)
@app.route("/places", methods=['GET'])
def get_places():
    # The main group of places to display to the user. Contains basic information
    # about the place and allows enough information to get more detailed information
    # or perform operations with the user and the place. 

    # connect to database
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()

    # create the query from the filters
    base_query = src.database.search_places()
    query_calls, arguments = _get_query()
    if any(query_calls):
        search_query = base_query + " WHERE " + " AND ".join((f"({call})" for call in query_calls if call != ""))
    else:
        search_query = base_query    

    # list of candidate places
    req = cursor.execute(search_query, arguments)
    places = (Place(x) for x in req)

    # get user preferences
    user = _load_user()
    # if len(ACTIVE_USERS) == 0:
    #     user = UserModel()
    #     user = get_user("user.json", user)
    #     ACTIVE_USERS[user.id] = user
    # else:
    #     user = ACTIVE_USERS["123"]

    # rank it baby
    ranking = rank_places(places, user)
    ranking.sort(key=lambda x: x[0], reverse=True)
    
    # going to return top 20 places, but can change later
    places_json = []

    # only top 20 for now, can change later
    for weight, place in ranking[:20]:
        places_json.append({
            "id":place.id,
            "name":place.display_name,
            "rating":place.rating,
            "priceLevel":place.price.value if place.price else None
        })

    conn.close()
    return jsonify(places_json)


@app.route("/place/<place_id>")
def _get_place(place_id):
    place_db = sqlite3.connect("places.db")
    place = src.database.get_place(place_db, place_id)
    place_json = {
        "id":place.id,
        "name":place.display_name,
        "rating":place.rating,
        "priceLevel":place.price,
        "primaryType": place.pt_display,
        "types": list(place.types),
        "priceLevel": place.price.value,
        "address": place.address,
        "website": place.website,
        "phone_number": place.phone_number
    }
    return jsonify(place_json)

# For use in displaying open time
@app.route("/place/<place_id>/time")
def _get_place_time(place_id):
    place_db = sqlite3.connect("places.db")
    hours = src.database.get_hours(place_db, place_id)
    return jsonify(hours.to_json())

def create_user():
    user = UserModel()
    user.id = "123"
    store_user("user.json", user)
    return user

@app.route("/save/<place_id>", methods=["POST"])
def add_saved(place_id):
    user = _get_user()
    try:
        conn = sqlite3.connect("places.db")
        place = src.database.get_place(conn, place_id)
        user.add_saved(place)
        store_user("user.json", user)
        return jsonify({"result": "Success"})
    except ValueError as e:
        return jsonify({"result": "ValueError", "errorMessage": str(e)})

@app.route("/like/<place_id>", methods=["POST"])
def add_liked(place_id):
    user = _get_user()
    try:
        conn = sqlite3.connect("places.db")
        place = src.database.get_place(conn, place_id)
        user.add_liked_place(place)
        store_user("user.json", user)
        return jsonify({"result": "Success"})
    except ValueError as e:
        return jsonify({"result": "ValueError", "errorMessage": str(e)})

@app.route("/visit/<place_id>", methods=["POST"])
def add_visited(place_id):
    user = _get_user()
    try:
        conn = sqlite3.connect("places.db")
        place = src.database.get_place(conn, place_id)
        user.add_visited(place)
        store_user("user.json", user)
        return jsonify({"result": "Success"})
    except ValueError as e:
        return jsonify({"result": "ValueError", "errorMessage": str(e)})

@app.route("/add_preference/<type>", methods=["POST"])
def add_preferred_type(type):
    user = _load_user()
    user.add_preferred_type(type)
    store_user("user.json", user)
    return jsonify({"result": "Success"})

@app.route("/unsave/<place_id>", methods=["POST"])
def remove_saved(place_id):
    user = _get_user()
    try:
        user.remove_saved(place_id)
        store_user("user.json")
        return jsonify({"result": "Success"})
    except KeyError as e:
        return jsonify({"result": "KeyError", "errorMessage": str(e)})

@app.route("/unlike/<place_id>", methods=["POST"])
def remove_liked(place_id):
    user = _get_user()
    try:
        user.remove_liked_place(place_id)
        store_user("user.json")
        return jsonify({"result": "Success"})
    except KeyError as e:
        return jsonify({"result": "KeyError", "errorMessage": str(e)})

# because visit is a history
@app.route("/unvisit/<index>", methods=["POST"])
def remove_visited(index):
    user = _get_user()
    try:
        user.remove_visited(index)
        store_user("user.json")
        return jsonify({"result": "Success"})
    except IndexError as e:
        return jsonify({"result": "KeyError", "errorMessage": str(e)})

@app.route("/remove_preference/<type>", methods=["POST"])
def remove_preferred_type(type):
    user = _load_user()
    try:
        user.remove_preferred_type(type)
        store_user("user.json", user)
        return jsonify({"result": "Success"})
    except KeyError as e:
        return jsonify({"result": "KeyError", "errorMessage": str(e)})

@app.route("/preferred_types", methods=["GET"])
def get_preferred_types():
    user = _load_user()
    return jsonify(list(user.preferred_types))

@app.get("/liked/")
def get_liked_places():
    user = _load_user()
    return jsonify([place.to_json() for place in user.liked_places])

@app.get("/saved/")
def get_saved_places():
    user = _load_user()
    return jsonify([place.to_json() for place in user.saved])

@app.get("/visited/")
def get_visited_places():
    user = _load_user()
    return jsonify([place.to_json() for place in user.visited])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
# @app.route("/...")
# def get_recommendation

# @app.route("/...")
# def search

# @app.route("/...")
# def 


