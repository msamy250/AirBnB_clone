#!/usr/bin/python3
"""Define State Class"""

from models.base_model import BaseModel


class State(BaseModel):
    """Initialize a new State instance.

    Args:
        name (str): State's name.
    """
    name = ""
