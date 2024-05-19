#!/usr/bin/python3
"""Define State Class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Initialize a new Review instance.

    Args:
        place_id (str): Review's place id.
        user_id (str): Review's user id.
        text (str): Review's text.
    """
    place_id = ""
    user_id = ""
    text = ""
