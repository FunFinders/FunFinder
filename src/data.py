from collections import namedtuple
from enum import Enum

class Price(Enum):
    PRICE_FREE = 0
    PRICE_INEXPENSIVE = 1
    PRICE_MODERATE = 2
    PRICE_EXPENSIVE = 3
    PRICE_VERY_EXPENSIVE = 4

Coordinates = namedtuple("Coordinates", "longitude latitude")
