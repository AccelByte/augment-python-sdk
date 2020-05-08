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

from justice import Justice
from . import JusticeTestCase


class JusticeWalletTestCase(JusticeTestCase):

    def setUp(self):
        """Create Justice object that can interact with Wallet."""
        super(JusticeWalletTestCase, self).setUp()
        self.user_id = "e3a07e0906794541954480740c1fb184"
        self.wallet_id = "e4f5141b712e490201712f1a7f9c001b"
    
    def test_get_wallet_by_id(self):
        resp = self.justice.wallet.get_wallet(self.wallet_id)
        result = resp.json()['id']

        self.assertEqual(result, self.wallet_id)
    
    def test_get_user_wallet(self):
        resp = self.justice.wallet.get_user_wallet(self.user_id, self.wallet_id)
        result = resp.json()

        self.assertEqual(result['id'], self.wallet_id)
        self.assertEqual(result['userId'], self.user_id)

    def test_get_wallet_by_currency(self):
        resp = self.justice.wallet.get_wallet_by_currency(self.user_id, 'USD')
        result = resp.json()['data'][0]

        self.assertEqual(result['userId'], self.user_id)

    def test_credit(self):
        resp = self.justice.wallet.credit(self.user_id, 100, 'USD')
        result = resp.json()

        self.assertEqual(result['userId'], self.user_id)
    
    def test_credit_balance(self):
        r1 = self.justice.wallet.get_user_wallet(self.user_id, self.wallet_id)
        balance = r1.json()['balance']

        self.justice.wallet.credit(self.user_id, 100, 'USD')

        r2 = self.justice.wallet.get_user_wallet(self.user_id, self.wallet_id)
        new_balance = r2.json()['balance']

        self.assertEqual(new_balance, balance + 100)
    
    def test_credit_in_transaction(self):
        self.justice.wallet.credit(self.user_id, 100, 'USD')
        resp = self.justice.wallet.get_transactions(self.user_id, self.wallet_id)
        result = resp.json()['data'][0]

        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['walletAction'], "CREDIT")
        self.assertEqual(result['currencyCode'], "USD")

    def test_debit(self):
        resp = self.justice.wallet.debit(self.user_id, 100, self.wallet_id)
        result = resp.json()

        self.assertEqual(result['userId'], self.user_id)

    def test_debit_balance(self):
        r1 = self.justice.wallet.get_user_wallet(self.user_id, self.wallet_id)
        balance = r1.json()['balance']

        self.justice.wallet.debit(self.user_id, 100, self.wallet_id)

        r2 = self.justice.wallet.get_user_wallet(self.user_id, self.wallet_id)
        new_balance = r2.json()['balance']

        self.assertEqual(new_balance, balance - 100)
    
    def test_debit_in_transaction(self):
        self.justice.wallet.debit(self.user_id, 100, self.wallet_id)
        resp = self.justice.wallet.get_transactions(self.user_id, self.wallet_id)
        result = resp.json()['data'][0]

        self.assertEqual(result['amount'], 100)
        self.assertEqual(result['walletAction'], "DEBIT")
        self.assertEqual(result['currencyCode'], "USD")

    def test_payment(self):
        resp = self.justice.wallet.pay(self.user_id, 100, "USD")
        result = resp.json()

        self.assertEqual(result['id'], self.wallet_id)
        self.assertEqual(result['userId'], self.user_id)
        # NOTE: is this sensible revert?
        self.justice.wallet.credit(self.user_id, 100, 'USD')
    
    def test_enable_wallet(self):
        resp = self.justice.wallet.enable(self.user_id, self.wallet_id)
        status_code = resp.status_code

        self.assertEqual(status_code, 204)

    def test_disable_wallet(self):
        resp = self.justice.wallet.disable(self.user_id, self.wallet_id)
        status_code = resp.status_code

        self.assertEqual(status_code, 204)
        # NOTE: is this sensible revert?
        self.justice.wallet.enable(self.user_id, self.wallet_id)

    def test_get_transactions(self):
        resp = self.justice.wallet.get_transactions(self.user_id, self.wallet_id)
        result = resp.json()['data'][0]

        self.assertEqual(result['walletId'], self.wallet_id)
        self.assertEqual(result['userId'], self.user_id)
