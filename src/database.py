from .data import OpeningHours, Place
from math import isclose
import sqlite3
import typing

def get_place(database, place_id):
    cursor = database.cursor()
    QUERY = """
    SELECT * from Places where place_id=:place_id
    """
    params = {"place_id": place_id}
    place_tuple = cursor.execute(QUERY, params).fetchone()
    if place_tuple is None:
        raise ValueError(f"place_id({place_id}) is not a valid place")
    return Place(place_tuple)

def get_hours(database, place_id):
    cursor = database.cursor()
    QUERY = """
    SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday from OpeningHours where place_id=:place_id
    """
    params = {"place_id": place_id}
    hours_tuple = cursor.execute(QUERY, params).fetchone()
    if hours_tuple is None:
        raise ValueError(f"place_id ({place_id}) is not present in Hours")
    return OpeningHours(hours_tuple)

def search_places():
    BASE_QUERY = "SELECT * FROM Places"
    return BASE_QUERY

def filter_price(min=0, max=4):
    if min == 0 and max == 4:
        return ""
    clause = ""
    if min != 0:
        clause = f"price >= {min}"
    if max != 4:
        if clause != "":
            clause += f" AND price <= {max}"
        else:
            clause = f"price <= {max}"
    return clause

def filter_type_disjunctive(types: list[str] | str):
    if type(types) is str:
        return f"instr(place_types, {types})"
    return " OR ".join((f"instr(place_types, \"{tag}\") > 0" for tag in types))

def filter_type_conjunctive(types: list[str] | str):
    if type(types) is str:
        return f"instr(place_types, {types})"
    return " AND ".join((f"instr(place_types, \"{tag}\") > 0" for tag in types))

def filter_rating(min: float=1.0, max: float=5.0):
    if min > max:
        raise ValueError("min is greater than max")
    # if min < 1.0:
    #     min = 1.0

    # if min > 5.0:
    #     min = 5.0

    # if max > 5.0:
    #     max = 5.0

    # if min > max:
    #     max = min

    QUERY = ""
    if not isclose(min, 1.0):
        QUERY = f"rating >= {min}"
    if not isclose(max, 5.0):
        if QUERY != "":
            QUERY += " AND "
        QUERY += f"rating <= {max}"
    return QUERY

def filter_():
    pass

def execute_query(query): 
    cnnx = sqlite3.connect("places.db")
    cursor = cnnx.cursor()
    result = cnnx.execute(query)
    return result

if __name__ == "__main__":
    query = search_places()
    calls = [filter_rating(2.2, 3.0), filter_type_conjunctive(["restaurant", "mexican_restaurant"]),
             filter_price(0, 2)]
    # print("\t\nAND ".join(call for call in calls if call != ""))
    print(query, "WHERE", " AND ".join(f"({call})" for call in calls if call != ""))
