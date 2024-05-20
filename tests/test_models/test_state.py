#!/usr/bin/python3
"""
Unit tests for the State class in models/state.py.

Test classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Tests for the instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(State(), State)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(State().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(State().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(State().updated_at, datetime)

    def test_name_is_public_class_attribute(self):
        st = State()
        self.assertIsInstance(State.name, str)
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def test_two_states_unique_ids(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_two_states_different_created_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_two_states_different_updated_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        st_str = str(st)
        self.assertIn("[State] (123456)", st_str)
        self.assertIn("'id': '123456'", st_str)
        self.assertIn("'created_at': " + dt_repr, st_str)
        self.assertIn("'updated_at': " + dt_repr, st_str)

    def test_args_unused(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at.isoformat(), dt_iso)
        self.assertEqual(st.updated_at.isoformat(), dt_iso)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Tests for the save method of the State class."""

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
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def test_two_saves(self):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def test_save_with_arg_raises_error(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_save_updates_file(self):
        st = State()
        st.save()
        st_id = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(st_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Tests for the to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertIsInstance(State().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        st = State()
        st_dict = st.to_dict()
        self.assertIn("id", st_dict)
        self.assertIn("created_at", st_dict)
        self.assertIn("updated_at", st_dict)
        self.assertIn("__class__", st_dict)

    def test_to_dict_contains_added_attributes(self):
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        self.assertEqual(st.middle_name, "Holberton")
        self.assertIn("my_number", st.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        st = State()
        st_dict = st.to_dict()
        self.assertIsInstance(st_dict["id"], str)
        self.assertIsInstance(st_dict["created_at"], str)
        self.assertIsInstance(st_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def test_to_dict_with_arg_raises_error(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
