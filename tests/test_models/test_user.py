#!/usr/bin/python3
"""
Unit tests for the User class in models/user.py.

Test classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Tests for the instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(User(), User)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(User().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(User().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(User().updated_at, datetime)

    def test_email_is_public_str(self):
        self.assertIsInstance(User.email, str)

    def test_password_is_public_str(self):
        self.assertIsInstance(User.password, str)

    def test_first_name_is_public_str(self):
        self.assertIsInstance(User.first_name, str)

    def test_last_name_is_public_str(self):
        self.assertIsInstance(User.last_name, str)

    def test_two_users_unique_ids(self):
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def test_two_users_different_created_at(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def test_two_users_different_updated_at(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        us_str = str(us)
        self.assertIn("[User] (123456)", us_str)
        self.assertIn("'id': '123456'", us_str)
        self.assertIn("'created_at': " + dt_repr, us_str)
        self.assertIn("'updated_at': " + dt_repr, us_str)

    def test_args_unused(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at.isoformat(), dt_iso)
        self.assertEqual(us.updated_at.isoformat(), dt_iso)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Tests for the save method of the User class."""

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

    def test_one_save(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_two_saves(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def test_save_with_arg_raises_error(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_updates_file(self):
        us = User()
        us.save()
        us_id = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(us_id, f.read())


class TestUserToDict(unittest.TestCase):
    """Tests for the to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertIsInstance(User().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        us = User()
        us_dict = us.to_dict()
        self.assertIn("id", us_dict)
        self.assertIn("created_at", us_dict)
        self.assertIn("updated_at", us_dict)
        self.assertIn("__class__", us_dict)

    def test_to_dict_contains_added_attributes(self):
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 98
        self.assertEqual(us.middle_name, "Holberton")
        self.assertIn("my_number", us.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        us = User()
        us_dict = us.to_dict()
        self.assertIsInstance(us_dict["id"], str)
        self.assertIsInstance(us_dict["created_at"], str)
        self.assertIsInstance(us_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dict_with_arg_raises_error(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
