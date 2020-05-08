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

import os
import unittest

from justice import Justice


class JusticeTestCase(unittest.TestCase):
    """Justice Test Case Super Class

    This class will handle the chore to setup and clean
    the testing process.
    """

    @classmethod
    def setUpClass(cls):
        try:
            cls.client_id = os.environ["IAM_CLIENT_ID"]
            cls.client_secret = os.environ["IAM_CLIENT_SECRET"]
        except KeyError:
            raise Exception(
                "IAM_CLIENT_ID and IAM_CLIENT_SECRET "
                "must be set in environment variables."
            )
        cls.test_users = []
        cls.namespace = 'accelbyte'
        cls.endpoint = "https://demo.accelbyte.io"
        cls.justice = Justice(cls.namespace, cls.endpoint)

    @classmethod
    def tearDownClass(cls):
        cls.justice.session.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass
