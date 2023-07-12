from rauth import OAuth2Service
from urllib.parse import parse_qsl
import hashlib
import os


class WakatimeAPI:
    """
    Class for work with WakaTime API

    https://wakatime.com/developers

    Attributes:
        client_id (str): Client ID from WakaTime
        client_secret (str): Client Secret from WakaTime
        session (rauth.session): Session for work with WakaTime API
        authorize_url (str): URL for authorization
        access_token_url (str): URL for get access token
        base_url (str): Base URL for WakaTime API
        redirect_uri (str): Redirect URI for WakaTime API
        headers (dict): Headers for WakaTime API


    Methods:
        get_url_auth: Get URL for authorization
        set_auth_session: Set session for work with WakaTime API
        refresh_session: Refresh session for work with WakaTime API
        get_refresh_token: Get refresh token
        get_access_token: Get access token
    """

    session = None
    authorize_url = "https://wakatime.com/oauth/authorize"
    access_token_url = "https://wakatime.com/oauth/token"
    base_url = "https://wakatime.com/api/v1/"
    redirect_uri = "https://wakatime.com/oauth/test"
    headers = {"Accept": "application/x-www-form-urlencoded"}

    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.service = OAuth2Service(
            client_id=self.client_id,
            client_secret=self.client_secret,
            name="wakatime",
            authorize_url=self.authorize_url,
            access_token_url=self.access_token_url,
            base_url=self.base_url,
        )
        self.state = hashlib.sha1(os.urandom(40)).hexdigest()

    def get_url_auth(self) -> str:
        """Get URL for authorization

        https://wakatime.com/developers#authentication

        Returns:
            str: URL for authorization
        """
        params = {
            "scope": "email,read_stats",
            "response_type": "code",
            "state": self.state,
            "redirect_uri": self.redirect_uri,
        }

        url = self.service.get_authorize_url(**params)

        return url

    def set_auth_session(self, code) -> bool:
        """Set session for work with WakaTime API

        https://wakatime.com/developers#authentication

        Args:
            code (str): Code for authorization

        Returns:
            bool: True if session is set, else False
        """

        try:
            self.session = self.service.get_auth_session(
                headers=self.headers,
                data={
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri,
                },
            )
        except KeyError:
            return False

        return True

    def refresh_session(self) -> None:
        """Refresh session for work with WakaTime API

        https://wakatime.com/developers#authentication
        """
        refresh_token = dict(parse_qsl(self.session.access_token_response.text))[
            "refresh_token"
        ]

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        self.session = self.service.get_auth_session(data=data)

    def _new_refresh_session(self, refresh_token) -> None:
        """Refresh session for work with WakaTime API

        https://wakatime.com/developers#authentication

        Args:
            refresh_token (str): Refresh token
        """

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        self.session = self.service.get_auth_session(data=data)

    def get_refresh_token(self) -> str:
        """Get refresh token

        https://wakatime.com/developers#authentication

        Returns:
            str: Refresh token
        """
        return dict(parse_qsl(self.session.access_token_response.text))["refresh_token"]

    def get_access_token(self) -> str:
        """Get access token

        https://wakatime.com/developers#authentication

        Returns:
            str: Access token
        """
        return dict(parse_qsl(self.session.access_token_response.text))["access_token"]

    def check_refresh_token(self, refresh_token) -> bool:
        """Check refresh token

        https://wakatime.com/developers

        Args:
            refresh_token (str): Refresh token

        Returns:
            bool: True if refresh token is valid, else False
        """

        self._new_refresh_session(refresh_token)

        try:
            self.session.get("users/current")
        except KeyError:
            return False

        return True


class WakatimeStats(WakatimeAPI):
    """
    Class based class WakatimeAPI for get statistics from WakaTime API

    https://wakatime.com/developers

    Methods:
        get_stats: Get all statistics
        get_lang_stats: Get statistics by languages
        get_all_time: Get all time
        get_os_stats: Get statistics by operating systems
        get_editors_stats: Get statistics by editors
        get_categories_stats: Get statistics by categories
    """

    def __init__(self, client_id, client_secret) -> None:
        super(WakatimeStats, self).__init__(client_id, client_secret)

    def get_stats(self) -> dict:
        """Get statistics

        https://wakatime.com/developers#stats

        Returns:
            dict: Statistics

        Raises:
            KeyError: If session is None
        """
        return self.session.get("users/current/stats").json()

    @staticmethod
    def new_refresh_session(refresh):
        """Decorator for refresh session

        Args:
            refresh (func): Function for refresh session

        Returns:
            func: Wrapper for refresh session
        """

        def wrapper(self, refresh_token):
            self._new_refresh_session(refresh_token)
            return refresh(self, refresh_token)

        return wrapper

    @new_refresh_session
    async def get_lang_stats(self, refresh_token):
        """Get statistics by languages

        https://wakatime.com/developers#stats

        Args:
            refresh_token (str): Refresh token

        Returns:
            dict: Statistics by languages
        """

        return self.get_stats()["data"]["languages"]

    @new_refresh_session
    async def get_all_time(self, refresh_token):
        """Get all time

        https://wakatime.com/developers#stats

        Args:
            refresh_token (str): Refresh token

        Returns:
            str: All time
        """
        return self.get_stats()["data"]["human_readable_total_including_other_language"]

    @new_refresh_session
    async def get_os_stats(self, refresh_token):
        """Get statistics by operating systems

        https://wakatime.com/developers#stats

        Args:
            refresh_token (str): Refresh token

        Returns:
            dict: Statistics by operating systems
        """
        return self.get_stats()["data"]["operating_systems"]

    @new_refresh_session
    async def get_editors_stats(self, refresh_token):
        """Get statistics by editors

        https://wakatime.com/developers#stats

        Args:
            refresh_token (str): Refresh token

        Returns:
            dict: Statistics by editors
        """
        return self.get_stats()["data"]["editors"]

    @new_refresh_session
    async def get_categories_stats(self, refresh_token):
        """Get statistics by categories

        https://wakatime.com/developers#stats

        Args:
            refresh_token (str): Refresh token

        Returns:
            dict: Statistics by categories
        """
        return self.get_stats()["data"]["categories"]
