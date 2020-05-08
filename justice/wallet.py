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

import json
import requests


# TODO: handling errorCode from backend
# TODO: move from returning response object to plain directory by .json() method
# TODO: do we wrap public method too?
class Wallet(object):
    """Accelbyte Wallet (Platform) Service

    lots of methods that interact with Wallet Service

    Args:
        namespace (str): namespace
        session (requests.Session): session that being used
        endpoint (str): API Endpoint URL
    
    Attributes:
        namespace (str)
        session (requests.Session)
    """
    WALLET_BODY_SOURCE = ['PURCHASE', 'IAP', 'PROMOTION',
                          'ACHIEVEMENT', 'REFERRAL_BONUS',
                          'REDEEM_CODE', 'REFUND', 'OTHER']

    def __init__(self, namespace, session, endpoint):
        self.namespace = namespace
        self.session = session
        self.base_url = endpoint
        self.admin_url = "{base}/platform/admin/namespaces/{namespace}".format(
            base=self.base_url, namespace=namespace)
        self.public_url = "{base}/platform/public/namespaces/{namespace}".format(
            base=self.base_url, namespace=namespace)
    
    def get_wallet(self, wallet_id):
        """Get a wallet by its id

        Args:
            wallet_id (int): wallet id
        
        Returns:
            requests.Response
        """
        url = "{base}/wallets/{wallet_id}".format(
            base=self.admin_url,
            wallet_id=wallet_id
        )
        return self.session.get(url)
    
    def get_user_wallet(self, user_id, wallet_id):
        """Get a wallet by its id within a user

        Args:
            user_id (int): user id
            wallet_id (int): wallet id
        
        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{wallet_id}".format(
            base=self.admin_url,
            user_id=user_id,
            wallet_id=wallet_id
        )
        return self.session.get(url)
    
    def get_wallet_by_currency(self, user_id, currency):
        """Get a user wallet info by currency code

        Args:
            user_id (int): user id
            currency (str): country currency ISO code
        
        Returns:
            requests.Response
        """
        url = "{base}/wallets".format(base=self.admin_url)

        payload = {
            'userId': user_id,
            'currencyCode': currency
        }
        return self.session.get(url, params=payload)

    def credit(self, user_id, amount, currency,
               source="PURCHASE", reason="augment-default"):
        """Credit a user wallet by currency code
        
        If wallet not exists, it will create a new wallet.

        Args:
            user_id (int): user id
            amount (int): amount being credit
            currency (str): country currency ISO code
            source (str, optional): source
            reason (str, optional): reason

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{currency}/credit".format(
            base=self.admin_url,
            user_id=user_id,
            currency=currency
        )

        # TODO: better handling for optional value of `source` and `reason`
        body = json.dumps({
            'amount': amount,
            'source': source,
            'reason': reason
        })
        return self.session.put(url, data=body)
    
    def debit(self, user_id, amount, wallet_id, reason="augment-default"):
        """Debit a user wallet

        Args:
            user_id (int): user id
            amount (int): amount being credit
            wallet_id (int): wallet id
            reason (str, optional): reason

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{wallet_id}/debit".format(
            base=self.admin_url,
            user_id=user_id,
            wallet_id=wallet_id
        )

        body = json.dumps({
            'amount': amount,
            'reason': reason
        })
        return self.session.put(url, data=body)

    def pay(self, user_id, amount, currency):
        """Pay with user wallet by currency code

        Args:
            user_id (int): user id
            amount (int): amount being credit
            currency (str): country currency ISO code

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{currency}/payment".format(
            base=self.admin_url,
            user_id=user_id,
            currency=currency
        )

        body = json.dumps({ 'amount': amount })
        return self.session.put(url, data=body)
    
    def enable(self, user_id, wallet_id):
        """Enable a user wallet

        Args:
            user_id (int): user id
            wallet_id (int): wallet id
        
        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{wallet_id}/enable".format(
            base=self.admin_url,
            user_id=user_id,
            wallet_id=wallet_id
        )
        return self.session.put(url)

    def disable(self, user_id, wallet_id):
        """Disable a user wallet

        Args:
            user_id (int): user id
            wallet_id (int): wallet id
        
        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/wallets/{wallet_id}/disable".format(
            base=self.admin_url,
            user_id=user_id,
            wallet_id=wallet_id
        )
        return self.session.put(url)
    
    def get_transactions(self, user_id, wallet_id):
        """List user wallet transactions ordered by create time
        in descending manner

        Args:
            user_id (int): user id
            wallet_id (int): wallet id
        
        Returns:
            requests.Response        
        """
        url = "{base}/users/{user_id}/wallets/{wallet_id}/transactions".format(
            base=self.admin_url,
            user_id=user_id,
            wallet_id=wallet_id
        )
        return self.session.get(url)
