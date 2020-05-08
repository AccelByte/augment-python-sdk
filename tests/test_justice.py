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
