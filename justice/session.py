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

import base64
import requests


class Session(object):
    """Session Manager

    An object to manage the current active session to call to the backend

    Args:
        client_id (str): IAM client id
        client_secret (str): IAM client secret
        endpoint (str): API Endpoint URL
    
    Attributes
        client_id (str)
        client_secret (str)
        session (requests.Session)
    """
    def __init__(self, client_id=None, client_secret=None, endpoint=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = endpoint
        self.grant_request_headers = self.__create_basic_auth_headers()
        self.session = requests.Session()

    def __create_basic_auth_headers(self):
        """Create basic auth headers

        Returns:
            headers with Basic Authorization
        """
        access_key = "{0}:{1}".format(self.client_id, self.client_secret)
        salted_key = base64.b64encode(
            access_key.encode("utf-8")).decode("utf-8")
        basic_auth = "Basic {0}".format(salted_key)
        headers = {'Authorization': basic_auth}
        return headers
    
    def init_client_credentials_grant(self):
        """Get grant by client credential

        Returns:
            requests.Session
        """
        token_url = "{0}/iam/oauth/token".format(self.base_url)
        grant_request_body = {
            'grant_type': 'client_credentials',
            'username': '',
            'password': '',
            'refresh_token': '',
            'code': '',
            'redirect_url': '',
            'namespace': ''
        }

        response = requests.post(token_url,
            data=grant_request_body, headers=self.grant_request_headers)
        token = response.json()

        self.session.headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "Bearer {0}".format(token['access_token'])
        }
        return self.session

    def init_password_grant(self, username, password):
        """Get grant by password

        Args:
            username (str)
            password (str)

        Returns:
            requests.Session
        """
        token_url = "{0}/iam/oauth/token".format(self.base_url)
        grant_request_body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'refresh_token': '',
            'code': '',
            'redirect_url': '',
            'namespace': ''
        }

        response = requests.post(token_url,
            data=grant_request_body, headers=self.grant_request_headers)
        token = response.json()

        self.session.headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "Bearer {0}".format(token['access_token'])
        }
        return self.session
