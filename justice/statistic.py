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


# NOTE: we only wrap admin methods for now
class Statistic(object):
    """Accelbyte Statistic Service

    This object provides wrapped methods to do CRUD operations to
    Justice Statistic Service.

    Args:
        namespace (str): Namespace
        session (requests.Session): Session that being used.
        endpoint (str): API Endpoint URL

    Attributes:
        namespace (str)
        session (requests.Session)
    """

    def __init__(self, namespace, session, endpoint):
        self.namespace = namespace
        self.session = session
        self.base_url = endpoint
        self.admin_url = "{base}/statistic/v1/admin/namespaces/{namespace}".format(
            base=self.base_url, namespace=namespace)
        self.public_url = "{base}/statistic/v1/public/namespaces/{namespace}".format(
            base=self.base_url, namespace=namespace)

    def get_global_stats(self):
        """List all global statItems by given namespace

        Returns:
            requests.Response
        """
        url = "{base}/globalstatitems".format(base=self.admin_url)
        return self.session.get(url)

    def search_statcode(self, keyword):
        """Query all stats by given namespace and stat code keyword

        Args:
            keyword (str): Stat code keyword.

        Returns:
            requests.Response
        """
        url = "{base}/stats/search".format(base=self.admin_url)
        payload = {'keyword': keyword}
        return self.session.get(url, params=payload)

    def get_stat_config(self, stat_code):
        """Get stat item configuration by its statCode

        Args:
            stat_code (str): statCode

        Returns:
            requests.Response
        """
        url = "{base}/stats/{stat_code}".format(
            base=self.admin_url,
            stat_code=stat_code
        )
        return self.session.get(url)

    def create_stat_config(self, config):
        """Create stat item configuration

        config example:
        ```python
        config = {
            "defaultValue": 0,
            "description": "string",
            "incrementOnly": True,
            "maximum": 0,
            "minimum": 0,
            "name": "string",
            "setAsGlobal": True,
            "setBy": "SERVER",
            "statCode": "string",
            "tags": [
                "string"
            ]
        }
        ```

        Args:
            stat_code (str): statCode
            config (dict): Stat configuration dict.

        Returns:
            requests.Response
        """
        url = "{base}/stats".format(base=self.admin_url)
        body = json.dumps(config)
        return self.session.post(url, data=body)

    def update_stat_config(self, stat_code, description=None, name=None, tags=None):
        """Update stat item configuration by its statCode

        Args:
            stat_code (str): statCode
            description (str, optional): Description to be updated. Defaults to None.
            name (str, optional): Name to be updated. Defaults to None.
            tags (str|list, optional): Tags to be updated. Defaults to None.

        Returns:
            requests.Response
        """
        url = "{base}/stats/{stat_code}".format(
            base=self.admin_url,
            stat_code=stat_code
        )
        payload = {}

        if description:
            payload['description'] = description
        if name:
            payload['name'] = name
        if tags and len(tags):
            if isinstance(tags, str):
                payload['tags'] = [tags]
            payload['tags'] = tags

        body = json.dumps(payload)
        return self.session.patch(url, data=body)

    def delete_stat_config(self, stat_code):
        """Delete a stat item configuration by its statCode

        Args:
            stat_code (str): Stat code that needs to be deleted.

        Returns:
            requests.Response
        """
        url = "{base}/stats/{stat_code}".format(
            base=self.admin_url,
            stat_code=stat_code
        )
        return self.session.delete(url)

    def get_user_stats(self, user_id):
        """Get the statistic for a user based on its id

        This will list all active statitems for that user

        Args:
            user_id (str): User id.

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/statitems".format(
            base=self.admin_url,
            user_id=user_id
        )
        return self.session.get(url)

    def create_user_statitem(self, user_id, stat_code):
        """Create a stat item for one user

        Args:
            user_id (str): User id.
            stat_code (str): statCode

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/stats/{stat_code}/statitems".format(
            base=self.admin_url,
            user_id=user_id,
            stat_code=stat_code
        )
        return self.session.post(url)

    def update_user_statitem_value(self, user_id, stat_code, value):
        """Update a stat item for a user

        Args:
            user_id (str): User id
            stat_code (str): statCode
            value (int): Stat item value to be updated.

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/stats/{stat_code}/statitems/value".format(
            base=self.admin_url,
            user_id=user_id,
            stat_code=stat_code
        )

        body = json.dumps({'inc': value})
        return self.session.patch(url, data=body)

    def delete_user_statitem(self, user_id, stat_code):
        """Delete a stat item for a user

        Args:
            user_id (str): User id
            stat_code (str): statCode

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/stats/{stat_code}/statitems".format(
            base=self.admin_url,
            user_id=user_id,
            stat_code=stat_code
        )
        return self.session.delete(url)

    def put_update_multiple_bulk(self, bulk):
        """Update multiple users' stats via PUT

        Scheme:
        ```python
        bulk = [
            {
                "inc": 0,
                "statCode": "string",
                "userId": "string"
            }
        ]
        ```

        Args:
            bulk (list of scheme): Bulk payloads.

        Returns:
            requests.Response
        """
        url = "{base}/statitems/value/bulk".format(base=self.admin_url)
        body = json.dumps(bulk)
        return self.session.put(url, data=body)

    def patch_update_multiple_bulk(self, bulk):
        """Update multiple users' stats via PATCH

        Scheme:
        ```python
        bulk = [
            {
                "inc": 0,
                "statCode": "string",
                "userId": "string"
            }
        ]
        ```

        Args:
            bulk (list of scheme): Bulk payloads.

        Returns:
            requests.Response
        """
        url = "{base}/statitems/value/bulk".format(base=self.admin_url)
        body = json.dumps(bulk)
        return self.session.patch(url, data=body)

    def create_single_bulk(self, user_id, bulk):
        """Bulk create stat items for one user

        The endpoint expect the payload to be like this:
        ```json
        [
            { "statCode": "string" }
        ]
        ```

        Args:
            bulk (list): list of statcode to be created

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/statitems/bulk".format(
            base=self.admin_url,
            user_id=user_id
        )

        payload = [{"statCode": item} for item in bulk]
        body = json.dumps(payload)
        return self.session.post(url, data=body)

    def put_update_single_bulk(self, user_id, bulk):
        """Bulk update one user stats via PUT

        Scheme:
        ```python
        bulk = [
            {
                "inc": 0,
                "statCode": "string"
            }
        ]
        ```

        Args:
            bulk (list of scheme): Bulk payloads.

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/statitems/value/bulk".format(
            base=self.admin_url,
            user_id=user_id
        )
        body = json.dumps(bulk)
        return self.session.put(url, data=body)

    def patch_update_single_bulk(self, user_id, bulk):
        """Bulk update one user stats via PATCH

        Scheme:
        ```python
        bulk = [
            {
                "inc": 0,
                "statCode": "string"
            }
        ]
        ```

        Args:
            bulk (list of scheme): Bulk payloads.

        Returns:
            requests.Response
        """
        url = "{base}/users/{user_id}/statitems/value/bulk".format(
            base=self.admin_url,
            user_id=user_id
        )
        body = json.dumps(bulk)
        return self.session.patch(url, data=body)
