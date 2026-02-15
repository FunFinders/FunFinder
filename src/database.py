from .data import OpeningHours, UserModel

def get_place(database, place_id):
    cursor = database.cursor()
    QUERY = """
    SELECT * from Places where place_id=:place_id
    """
    params = {"place_id": place_id}
    place_tuple = cursor.execute(QUERY, params).fetchone()
    return UserModel(place_tuple)

def get_hours(database, place_id):
    cursor = database.cursor()
    QUERY = """
    SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday from OpeningHours where place_id=:place_id
    """
    params = {"place_id": place_id}
    hours_tuple = cursor.execute(QUERY, params).fetchone()
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

def filter_():
    pass
