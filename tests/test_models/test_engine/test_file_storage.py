#!/usr/bin/python3
"""
Unit tests for FileStorage class in models/engine/file_storage.py.

Test classes:
    TestFileStorageInitialization
    TestFileStorageMethods
"""

import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInitialization(unittest.TestCase):
    """Tests for initializing the FileStorage class."""

    def test_no_args_instantiation(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_private_file_path_is_str(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_private_objects_is_dict(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initialization(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Tests for methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_adds_objects(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn(f"BaseModel.{bm.id}", models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn(f"User.{us.id}", models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn(f"State.{st.id}", models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn(f"Place.{pl.id}", models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn(f"City.{cy.id}", models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn(f"Amenity.{am.id}", models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn(f"Review.{rv.id}", models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_creates_file(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn(f"BaseModel.{bm.id}", save_text)
            self.assertIn(f"User.{us.id}", save_text)
            self.assertIn(f"State.{st.id}", save_text)
            self.assertIn(f"Place.{pl.id}", save_text)
            self.assertIn(f"City.{cy.id}", save_text)
            self.assertIn(f"Amenity.{am.id}", save_text)
            self.assertIn(f"Review.{rv.id}", save_text)

    def test_save_with_arg_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_populates_objects(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn(f"BaseModel.{bm.id}", objs)
        self.assertIn(f"User.{us.id}", objs)
        self.assertIn(f"State.{st.id}", objs)
        self.assertIn(f"Place.{pl.id}", objs)
        self.assertIn(f"City.{cy.id}", objs)
        self.assertIn(f"Amenity.{am.id}", objs)
        self.assertIn(f"Review.{rv.id}", objs)

    def test_reload_with_arg_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
