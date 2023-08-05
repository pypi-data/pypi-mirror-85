import json
import os
from .api_call import api_call, api_auth, NotFoundError, ServerError, UnauthorizedError
from .account import Account
from .user import User


class FreedomClient(object):
    """Freedom Robotics API client library. Instantiate this first and access all API functions from within a FreedomClient.

    You can instantiate a `FreedomClient` using either no arguments (in which case credentials are searched for in ~/.freedom_credentials), a `token` and `secret`, or a `username` and `password`.

    Args:
        token (str): API token. Can be a session or user token.
        secret (str): API secret.
        username (str): Username.
        password (str): Password.
    """

    def __init__(self, token =None, secret =None, username=None, password=None, url=None):
        # if class is initialized with a token and secret, use it
        if token is not None and secret is not None:
            self.token = token
            self.secret = secret
            api_auth(self.token, self.secret, url=url)

        # if class is initialized with a username and password, use it
        elif username is not None and password is not None:
            response = api_call("PUT", "/users/%s/login" % username, data = {
                "password": password
            }, no_auth = True)
            self.token = response.get("token")
            self.secret = response.get("secret")
            api_auth(self.token, self.secret, url=url)

        # if there is a saved freedom credentials file, use it
        elif os.path.exists(os.path.expanduser("~/.freedom_credentials")):
            with open(os.path.expanduser("~/.freedom_credentials")) as f:
                credentials = json.loads(f.read())
                if url is None:
                    url = credentials.get("url", "https://api.freedomrobotics.ai/")
                self.token = credentials.get("token")
                self.secret = credentials.get("secret")
                api_auth(self.token, self.secret, url=url)

        else:
            raise Exception("Required: either token/secret, username/password, or saved ~/.freedom_credentials file")

    def account(self, account_id):
        """:obj:`Account`: Fetch an account by its account ID (Axxxxxxxxxxxx).

        Args:
            account_id (str): Account ID.
        """

        account_data = api_call("GET", "/accounts/%s" % account_id)
        if not account_data:
            return None
        return Account(account_data["account"], account_data)

    @property
    def accounts(self):
        """:obj:`list` of :obj:`Account`: Fetch a list of all accounts that are visible/accessible.
        """

        result = api_call("GET", "/accounts")
        if not result:
            return None
        return [Account(account_data["account"], account_data) for account_data in result]

    @property
    def users(self):
        """:obj:`list` of :obj:`User`: Fetch a list of all users that are visible/accessible.
        """

        result = api_call("GET", "/users")
        if not result:
            return
        return [User(user_data["user"], user_data) for user_data in result]

    @property
    def tokens(self):
        """:obj:`list` of :obj:`dict`: Fetch a list of tokens.
        """

        result = api_call("GET", "/accounts")
        return result

