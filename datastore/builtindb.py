# Copyright 2020 AccelByte Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib.parse
import os

from pymongo import MongoClient


class BuiltInDB(object):
    """Python SDK for Augment Built-In Database

    This is singleton class to interact with Augment built-in database

    Args:
        namespace (str): Namespace
        endpoint (str): API endpoint URL

    Attributes:
        database: Python object tat interacts with built-in database
    """
    DEFAULT_MONGODB = "abcluster-accelbyte-prod-docdb-cluster-0.cfunpavjqvdi.us-west-2.docdb.amazonaws.com:27017/" + \
                      "?replicaSet=rs0&readPreference=secondaryPreferred"

    def __init__(self, endpoint=DEFAULT_MONGODB):
        # create mongoDB client session
        username = urllib.parse.quote_plus(os.environ['BUILTIN_DB_USER_NAME'])
        password = urllib.parse.quote_plus(os.environ['BUILTIN_DB_USER_PASSWORD'])
        db_name = urllib.parse.quote_plus(os.environ['BUILTIN_DB_NAME'])
        try:
            client = MongoClient('mongodb://%s:%s@%s' % (username, password, endpoint))

            # assign the database name
            self.database = client[db_name]
        except Exception as exception:
            raise exception

    def insert(self, collection_name, data):
        """Insert a dictionary of data to the built-in database

        Args:
            collection_name (string): name of the collection to insert the data into
            data (dict): data to insert

        Returns:
            data (dict)
        """
        try:
            self.database[collection_name].insert_one(data)
        except Exception as exception:
            raise exception

        return data

    def get(self, collection_name, get_filter={}):
        """Get data in a collection

        Args:
            collection_name (string): name of the collection to insert the data into
            get_filter (dict): filter dict to get data

        Returns:
            data (dict)
        """
        try:
            result_data = self.database[collection_name].find_one(get_filter)
        except Exception as exception:
            raise exception

        return result_data

    def update(self, collection_name, update_filter, new_data):
        """Update data in a collection by replacing with the new data

        Args:
            collection_name (string): name of the collection to insert the data into
            update_filter (dict): filter dict to get the data to be updated
            new_data (dict): new data to replace the existing data

        Returns:
            new_data (dict)
        """
        try:
            update_result = self.database[collection_name].replace_one(update_filter, new_data)
            if update_result.matched_count == 0:
                raise Exception("data to update not found")
        except Exception as exception:
            raise exception

        return new_data

    def delete(self, collection_name, delete_filter):
        """Update data in a collection by replacing with the new data

        Args:
            collection_name (string): name of the collection to insert the data into
            delete_filter (dict): filter dict to get the data to be deleted
        """
        try:
            self.database[collection_name].delete_one(delete_filter)
        except Exception as exception:
            raise exception

