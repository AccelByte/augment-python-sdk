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


class MongoDB(object):
    """Python SDK for Augment Built-In Database

    This is singleton class to interact with Augment built-in database

    Args:
        namespace (str): Namespace
        endpoint (str): API endpoint URL

    Attributes:
        database: Python object that interacts with built-in database
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
            self.builtin_db = client[db_name]
        except Exception as exception:
            raise exception

