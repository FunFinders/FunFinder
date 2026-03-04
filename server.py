from flask import Flask, jsonify
from flask_cors import CORS  # Add this import
from src.data import UserModel, Place
from src.recommendation import rank_places
from src.user import get_user
import sqlite3

# use jsonify
# make_response ... .set_cookie(key, value)?
# request.cookies?

app = Flask(__name__)
CORS(app)
@app.route("/places", methods=['GET'])

def get_places():
    # connect to database
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()

    # list of places
    req = cursor.execute("select * from places")
    places = [Place(x) for x in req]

    # get user preferences
    user = UserModel()
    user = get_user("user.json", user)

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
            "priceLevel":place.price
        })
    
    conn.close()
    return jsonify(places_json)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)



# def get_user():
#     pass

# @app.route("/...")
# def get_places():
#     pass

# @app.route("/...")
# def get_place():
#     pass

# @app.route("/...")
# def store_user():
#     pass

# @app.route("/...")
# def create_user():
#     pass

# @app.route("/...")
# def add_saved

# @app.route("/...")
# def add_liked

# @app.route("/...")
# def add_visited

# @app.route("/...")
# def add_preferred_type

# @app.route("/...")
# def remove_saved

# @app.route("/...")
# def remove_liked

# @app.route("/...")
# def remove_visited

# @app.route("/...")
# def remove_preferred_type

# @app.route("/...")
# def get_recommendation

# @app.route("/...")
# def search

# @app.route("/...")
# def 


