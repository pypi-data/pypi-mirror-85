__all__ = [
    "SpotifyClientCredentials",
    "SpotifyOAuth",
    "isTokenExpired"
]

from datetime import datetime, timedelta
from urllib.parse import urlencode
import json
import requests
import base64
import os
from spotiply.client import Spotify


class ClientCredentialsError(Exception):
    def __init__(self, http_status_code, message):
        self.http_status_code = http_status_code
        self.message = message

    def __str__(self):
        return f'http.status_code: {self.http_status_code},\
 message: {self.message}'


class OAuthError(Exception):
    def __init__(self, http_status_code, message):
        self.http_status_code = http_status_code
        self.message = message

    def __str__(self):
        return f'http.status_code: {self.http_status_code},\
 message: {self.message}'


class TokenNotExpired(Exception):
    def __init__(self, expires_at):
        self.expires_at = datetime.fromtimestamp(expires_at)

    def __str__(self):
        return f"Token not yet expired. Expires at {self.expires_at}"


class BaseAuth():

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 cache_path: str = None):
        self._client_id = client_id
        self._client_secret = client_secret
        self.cache_path = _get_cache_path(cache_path)

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        if client_id is None or "":
            raise ValueError("client_id cannot be empty.")
        self._client_id = client_id

    @property
    def client_secret(self):
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        if client_secret is None:
            raise ValueError("client_secret cannot be empty.")
        self._client_secret = client_secret

    def _authHeader(self):
        """Header Parameter

        Returns:
            dict: The Header
        """
        clientCredentials = f"{self.client_id}:{self.client_secret}"
        clientBase64 = base64.b64encode(clientCredentials.encode())
        return {
            "Authorization": f"Basic {clientBase64.decode()}"
        }


def isTokenExpired(token_info: dict):
    """Check if the token is expired

    Args:
        token_info (dict): Token information from cached token\
         or `getAccessToken()`

    Returns:
        bool: if the token is expired
    """
    now = datetime.now().timestamp()
    expires_at = token_info['expires_at']

    return now > expires_at


def _get_cache_path(cache_path: str = None):
    if cache_path:
        if not os.path.exists(cache_path):
            raise FileNotFoundError("Path Does not exist.")

        cache_path = os.path.join(cache_path, '.cache')

        return cache_path

    cache_path = '.cache'
    return cache_path


def _read_user_cache(cache_file: str, user: str = None):
    """Opens a cache file as 'read'

    Args:
        cache_file (str, optional): cache_path. Defaults to None.

    Returns:
        dict: token information
    """
    if user:
        cache_file += f'-{user}'

    with open(cache_file, 'r') as f:
        data = json.load(f)
    f.close()
    return dict(data)


def _requests(method, **kwargs):
    url = "https://accounts.spotify.com/api/token"

    return method(url, **kwargs)


class SpotifyClientCredentials(BaseAuth):
    """The Spotify Client Credentials"""
    _token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id: str,
                 client_secret: str,
                 cache_path: str = None):
        """Initialize the Spotify Client

        Don't have `client_id` and `client_secret`? Login to spotify, create\
        new integrations and manage your
        Spotify credentials at https://developer.spotify.com/dashboard/ .

        Args:
            client_id (str, required): Your Client ID
            client_secret (str, required): Your Client Secret
            cache_path (str, optional): Your cache path. Defaults\
            to your file's directory.
        """
        super().__init__(client_id, client_secret, cache_path)

    # Getters / Setters
    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @client_id.setter
    def client_id(self, client_id):
        if client_id is None or "":
            raise ValueError("client_id cannot be empty.")
        self._client_id = client_id

    @client_secret.setter
    def client_secret(self, client_secret):
        if client_secret is None:
            raise ValueError("client_secret cannot be empty.")
        self._client_secret = client_secret

    # Methods / Functions

    def _clientBody(self):
        """The Request Body Parameter

        Returns:
            dict: The Body
        """
        return {
            "grant_type": "client_credentials"
        }

    def getAccessToken(self):
        """The access token allows you to make request to the
        Spotify Web API endpoints that do not require user
        authorization.

        Raises:
            Exception: When something went wrong in the authentication
            or `client_id` or `client_secret` must be wrong.

        Returns:
            dict: The access token info in dict.
        """
        r = _requests(requests.post,
                      data=self._clientBody(),
                      headers=self._authHeader())

        if r.status_code != 200:
            raise ClientCredentialsError(r.status_code,
                                         "Couldn't authenticate client")
        else:
            token_info = r.json()
            expires_in = datetime.now() + timedelta(
                seconds=token_info['expires_in'])
            token_info.update(expires_at=expires_in.timestamp())

            with open(self.cache_path, 'w') as f:
                json.dump(token_info, f, indent=4)
            f.close()
            return dict(r.json())

    def getCachedToken(self):
        if not os.path.exists(self.cache_path):
            self.getAccessToken()
            return _read_user_cache(self.cache_path)
        else:
            return _read_user_cache(self.cache_path)


class SpotifyOAuth(BaseAuth):

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 cache_path: str = None,
                 state=None,
                 scope: str = None,
                 show_dialog=False):
        super().__init__(client_id, client_secret, cache_path)
        self._redirect_uri = redirect_uri
        self._state = state
        self._scope = scope
        self._show_dialog = show_dialog

    # Getters
    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def redirect_uri(self):
        return self._redirect_uri

    @property
    def state(self):
        return self._state

    @property
    def scope(self):
        return self._scope

    @property
    def show_dialog(self):
        return self._show_dialog

    # Setters
    @client_id.setter
    def client_id(self, client_id):
        if client_id is None or "":
            raise ValueError("client_id cannot be empty.")
        self._client_id = client_id

    @client_secret.setter
    def client_secret(self, client_secret):
        if client_secret is None or "":
            raise ValueError("client_secret cannot be empty.")
        self._client_secret = client_secret

    @redirect_uri.setter
    def redirect_uri(self, redirect_uri):
        if redirect_uri is None or "":
            raise ValueError("redirect_uri is a required query parameter. \
It cannot be empty.")
        self._redirect_uri = redirect_uri

    @state.setter
    def state(self, state):
        self._state = state

    @scope.setter
    def scope(self, scope: str):
        self._scope = scope

    @show_dialog.setter
    def show_dialog(self, show_dialog):
        self._show_dialog = show_dialog

    # Methods
    def getAuthorizeURL(self):
        OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
        query_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "show_dialog": self.show_dialog
        }
        if self.state:
            query_params['state'] = self.state
        if self.scope:
            query_params['scope'] = self.scope

        query_params = urlencode(query_params)

        return f"{OAUTH_AUTHORIZE_URL}?{query_params}"

    def _getUserName(self, access_token: str):
        """Get The user's display name from spotify

        Args:
            access_token (str): Their access token

        Returns:
            str: Their display name
        """
        sp = Spotify(access_token)
        user = sp.current_user()
        return user['id']

    def _oAuthBody(self, code: str):
        return {
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }

    def getAccessToken(self, code):
        """The access token allows you to make request to the
        Spotify Web API endpoints. Requires user authorizatoion.
        Scopes are optional.

        Args:
            code (str): code from the callback query_param link.

        Raises:
            OAuthError: When status code is not equal to 200.

        Returns:
            dict: Access Token Information
        """
        r = _requests(requests.post,
                      data=self._oAuthBody(code),
                      headers=self._authHeader())

        if r.status_code != 200:
            raise OAuthError(r.status_code,
                             "Couldn't authenticate client")
        else:
            token_info = r.json()
            expires_in = datetime.now() + timedelta(
                seconds=token_info['expires_in']
            )
            token_info.update(expires_at=expires_in.timestamp())
        user = self._getUserName(token_info['access_token'])

        with open(f"{self.cache_path}-{user}", 'w') as f:
            json.dump(token_info, f, indent=4)
        f.close()

        return token_info

    def refreshAccessToken(self, username: str):
        """Refresh the access_token

        Args:
            username (str): user's spotify id or username

        Raises:
            FileNotFoundError: If the cache token_info still not exist.
        """
        if not os.path.exists(f'{self.cache_path}-{username}'):
            raise FileNotFoundError("Cache doesn't exist. perform getAccessToken()\
 first.")
        else:
            token_info = _read_user_cache(self.cache_path, username)
            if not isTokenExpired(token_info):
                raise TokenNotExpired(token_info['expires_at'])
            else:
                refreshed_token = self._performRefresh(token_info)
                expires_in = datetime.now() + timedelta(
                    seconds=refreshed_token['expires_in']
                )
                if 'refresh_token' not in refreshed_token:
                    refreshed_token.update(
                        refresh_token=token_info['refresh_token']
                    )
                refreshed_token.update(expires_at=expires_in.timestamp())

                with open(f'{self.cache_path}-{username}', 'w') as f:
                    json.dump(refreshed_token, f, indent=4)
                f.close()
                return refreshed_token

    def _performRefresh(self, token_info: dict):
        url = 'https://accounts.spotify.com/api/token'
        authOptions = {
            'grant_type': 'refresh_token',
            'refresh_token': token_info["refresh_token"]
        }
        r = requests.post(url,
                          data=authOptions,
                          headers=self._authHeader())
        if r.status_code == 200:
            return dict(r.json())
        else:
            return r.status_code
