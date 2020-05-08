# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

import requests

from justice import Justice
from justice.wallet import Wallet
from justice.statistic import Statistic
from . import JusticeTestCase


class JusticeCoreTestCase(JusticeTestCase):

    def test_session_instance(self):
        self.assertIsInstance(self.justice.session, requests.Session)

    def test_wallet_instance(self):
        self.assertIsInstance(self.justice.wallet, Wallet)

    def test_statistic_instance(self):
        self.assertIsInstance(self.justice.statistic, Statistic)

    def test_valid_url(self):
        url = "https://demo.accelbyte.io"
        self.assertTrue(self.justice.valid_url(url))

    def test_invalid_url(self):
        url = "asem"
        self.assertFalse(self.justice.valid_url(url))
