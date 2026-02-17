from src.data import UserModel, Place
from src.recommendation import *
from src.database import *
from src.user import *
import sqlite3

conn = sqlite3.connect("places.db")
cursor = conn.cursor()
req = cursor.execute("select * from places")
places = [Place(x) for x in req]
user = UserModel()
user = get_user("user.json", user)


ranking = rank_places(places, user)
ranking.sort(key=lambda a: a[0], reverse=True)

for place in ranking:
    print(place[0], place[1].display_name)