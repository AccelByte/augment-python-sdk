# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

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
