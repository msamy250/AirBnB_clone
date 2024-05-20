#!/usr/bin/python3
"""
Unit tests for the HBNB command interpreter in console.py.

Test classes:
    TestHBNBCommandPrompting
    TestHBNBCommandHelp
    TestHBNBCommandExit
    TestHBNBCommandCreate
    TestHBNBCommandShow
    TestHBNBCommandDestroy
    TestHBNBCommandAll
    TestHBNBCommandUpdate
"""

import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandPrompting(unittest.TestCase):
    """Tests for the prompting behavior of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandHelp(unittest.TestCase):
    """Tests for the help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        expected = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_create(self):
        expected = ("Usage: create <class>\n        "
                    "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_EOF(self):
        expected = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_show(self):
        expected = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
                    "Display the string representation of a class instance of"
                    " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_destroy(self):
        expected = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
                    "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_all(self):
        expected = ("Usage: all or all <class> or <class>.all()\n        "
                    "Display string representations of all instances of a given class"
                    ".\n        If no class is specified, displays all instantiated "
                    "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_count(self):
        expected = ("Usage: count <class> or <class>.count()\n        "
                    "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help_update(self):
        expected = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
                    "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
                    ">) or\n       <class>.update(<id>, <dictionary>)\n        "
                    "Update a class instance of a given id by adding or updating\n   "
                    "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_help(self):
        expected = ("Documented commands (type help <topic>):\n"
                    "========================================\n"
                    "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(expected, output.getvalue().strip())


class TestHBNBCommandExit(unittest.TestCase):
    """Tests for exiting the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandCreate(unittest.TestCase):
    """Tests for the create command of the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missing_class(self):
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_create_invalid_class(self):
        expected = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        expected = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(expected, output.getvalue().strip())
        expected = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "User.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "State.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "City.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "Place.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            test_key = "Review.{}".format(output.getvalue().strip())
            self.assertIn(test_key, storage.all().keys())


class TestHBNBCommandShow(unittest.TestCase):
    """Tests for the show command of the HBNB command interpreter."""

    @classmethod
