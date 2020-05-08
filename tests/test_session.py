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
from justice.session import Session


class JusticeSessionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_id = os.environ["IAM_CLIENT_ID"]
        cls.client_secret = os.environ["IAM_CLIENT_SECRET"]
        cls.endpoint = "https://demo.accelbyte.io"
        cls.justice = Justice(
            'accelbyte', endpoint=cls.endpoint)

    @classmethod
    def tearDownClass(cls):
        cls.justice.session.close()

    def test_created_accept_header(self):
        header = self.justice.session.headers['Accept']
        self.assertEqual(header, 'application/json')

    def test_created_content_type_header(self):
        header = self.justice.session.headers['content-type']
        self.assertEqual(header, 'application/json')

    def test_created_auth_bearer_header(self):
        header = self.justice.session.headers['Authorization']
        self.assertIsNotNone(header)

    def test_getting_grant_by_password(self):
        sess = Session(client_id=self.client_id,
                       client_secret=self.client_secret,
                       endpoint=self.endpoint)
        username = os.environ['ADMIN_USERNAME']
        password = os.environ['ADMIN_PASSWORD']
        session = sess.init_password_grant(username, password)
        auth_header = session.headers['Authorization']

        self.assertEqual(auth_header.startswith('Bearer'), True)

    def test_getting_grant_by_client_credentials(self):
        sess = Session(client_id=self.client_id,
                       client_secret=self.client_secret,
                       endpoint=self.endpoint)
        session = sess.init_client_credentials_grant()
        auth_header = session.headers['Authorization']

        self.assertEqual(auth_header.startswith('Bearer'), True)
