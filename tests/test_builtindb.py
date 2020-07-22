import unittest
import os

from pymongo import MongoClient
from datastore import BuiltInDB


class BuiltInDBTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builtin_database = BuiltInDB(endpoint="mongodb:27017")
        cls.mongo_client = MongoClient('mongodb://mongouser:mongopass@mongodb:27017')

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_insert_success(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}
        mongo_client_db = self.mongo_client[os.environ['BUILTIN_DB_NAME']]

        inserted_data = self.builtin_database.insert(test_collection, test_data)
        get_result_data = mongo_client_db[test_collection].find_one(test_data)

        self.assertEqual(test_data, inserted_data)
        self.assertEqual(test_data["name"], get_result_data["name"])

        mongo_client_db[test_collection].delete_one(test_data)

    def test_get_success(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}
        mongo_client_db = self.mongo_client[os.environ['BUILTIN_DB_NAME']]
        mongo_client_db[test_collection].insert_one(test_data)

        get_data = self.builtin_database.get(test_collection, test_data)

        self.assertEqual(test_data["name"], get_data["name"])

        mongo_client_db[test_collection].delete_one(test_data)

    def test_get_not_found(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}

        get_data = self.builtin_database.get(test_collection, test_data)

        self.assertIsNone(get_data)

    def test_update_success(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}
        mongo_client_db = self.mongo_client[os.environ['BUILTIN_DB_NAME']]
        mongo_client_db[test_collection].insert_one(test_data)
        new_data = {"name": "new_test", "address": "test_address"}

        updated_data = self.builtin_database.update(test_collection, test_data, new_data)

        self.assertEqual(new_data["name"], updated_data["name"])

        mongo_client_db[test_collection].delete_one(new_data)

    def test_update_not_found(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}
        new_data = {"name": "new_test", "address": "test_address"}

        with self.assertRaisesRegex(Exception, "data to update not found"):
            self.builtin_database.update(test_collection, test_data, new_data)

    def test_delete_success(self):
        test_collection = "testcollection"
        test_data = {"name": "test", "address": "test address"}
        mongo_client_db = self.mongo_client[os.environ['BUILTIN_DB_NAME']]
        mongo_client_db[test_collection].insert_one(test_data)

        error = self.builtin_database.delete(test_collection, test_data)

        self.assertIsNone(error)
