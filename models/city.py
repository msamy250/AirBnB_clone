#!/usr/bin/python3
"""Define city Class"""

from models.base_model import BaseModel


class City(BaseModel):
    """Initialize a new City instance.

    Args:
        state_id (str): City's state id.
        name (str): City's name.
    """
    state_id = ""
    name = ""
