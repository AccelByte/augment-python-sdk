import unittest
import os

from pymongo import MongoClient
from datastore import MongoDB


class BuiltInDBTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.augment_mongodb = MongoDB(endpoint="mongodb:27017")
        username = os.environ['BUILTIN_DB_USER_NAME']
        password = os.environ['BUILTIN_DB_USER_PASSWORD']
        cls.mongo_client = MongoClient('mongodb://%s:%s@mongodb:27017' % (username, password))

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_database_pointing(self):
        mongo_client_db = self.mongo_client[os.environ['BUILTIN_DB_NAME']]
        collection_name = "samplecollection"
        mongo_client_db[collection_name].insert_one({"some": "test"})
        get_result = self.augment_mongodb.builtin_db[collection_name].find_one({"some": "test"})
        get_result.pop('_id', None)

        self.assertEqual({"some": "test"}, get_result)
