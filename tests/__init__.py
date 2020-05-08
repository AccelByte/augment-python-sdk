# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

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
