#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUp(self):
        """Setup for the tests"""
        models.storage.reload()
        self.session = models.storage._DBStorage__session

    @classmethod
    def tearDown(self):
        """Destroy the fixtures"""
        self.session.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_items = models.storage.all()
        all_from_db = {}
        for cls in classes:
            for row in self.session.query(classes[cls]).all():
                all_from_db[row.id] = row

        self.assertEqual(all_items, all_from_db)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        details = {'password': 'heiisa', 'email': 'joe@me.com'}
        my_obj = User(**details)
        models.storage.new(my_obj)
        self.assertEqual(my_obj, self.session.query(User).
                         filter(User.id == my_obj.id).first())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retreives the correct object"""
        details = {'password': 'heiisa', 'email': 'joe@me.com'}
        my_obj = User(**details)
        my_obj.save()
        self.session.close()
        models.storage.reload()
        self.assertEqual(my_obj.email, models.storage.get(User, my_obj.id).
                         email)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_fake_object(self):
        """Test that get retreives the correct object"""
        self.assertEqual(None, models.storage.get(Place, 'fake'))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_without_class(self):
        """Test count method without a class given"""
        count = len(models.storage.all())
        self.assertEqual(count, models.storage.count())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_class(self):
        """Test count method without a class given"""
        all_objs = models.storage.all()
        cls = User
        cls_count = 0
        for item in all_objs.keys():
            if item.split('.')[0] == cls.__name__:
                cls_count += 1
        self.assertEqual(cls_count, models.storage.count(cls))
