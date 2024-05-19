#!/usr/bin/python3
"""Define city Class"""

from models.base_model import BaseModel


class Place(BaseModel):
    """Initialize a new Place instance.

    Args:
        city_id (str): Place's city id.
        user_id (str): Place's user id.
        name(str): Place's name.
        description (str): Place's description.
        number_rooms (int): Place's number of rooms.
        number_bathrooms (int): Place's number of bathrooms.
        max_guest (int): Place's max guest.
        price_by_night (int): Place's price per night.
        latitude (float): Place's latitude.
        longitude (float): Place's longitude.
        amenity_ids (list): Place's amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
