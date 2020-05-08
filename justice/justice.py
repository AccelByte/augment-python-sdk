# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

import os
import re
import requests

from .session import Session
from .wallet import Wallet
from .statistic import Statistic


class Justice(object):
    """Justice Python SDK for Augment

    This is singleton class to interact with other justice service objects

    Args:
        namespace (str): Namespace
        endpoint (str): API endpoint URL

    Attributes:
        session (requests.Session): Python `requests.Session` object that is
            currently active.
        wallet (justice.Wallet): Wallet object to interact with Justice Wallet
            Service.
        statistic (justice.Statistic): Statistic object to interact with justice
            Statistic Service.
    """
    DEFAULT_ENDPOINT = "https://demo.accelbyte.io"

    def __init__(self, namespace, endpoint=DEFAULT_ENDPOINT):
        if not self.valid_url(endpoint):
            message = "{} is not a valid API endpoint URL".format(endpoint)
            raise ValueError(message)

        # create session
        client_id = os.environ['IAM_CLIENT_ID']
        client_secret = os.environ['IAM_CLIENT_SECRET']
        sess = Session(client_id, client_secret, endpoint)

        # init session with client credentials to get grant token
        self.session = sess.init_client_credentials_grant()

        # initialise accelbyte services objects
        self.__init_services_object(namespace, endpoint)

    def __init_services_object(self, namespace, endpoint):
        """Private method to expose available service objects"""
        self.wallet = Wallet(namespace, self.session, endpoint)
        self.statistic = Statistic(namespace, self.session, endpoint)

    def valid_url(self, url):
        """Check if given string is a valid URL scheme.

        Args:
            url (str): string that contains URL to be checked.

        Returns:
            re.Match object, None otherwise.
        """
        pattern = re.compile(
            r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
        return pattern.match(url)
