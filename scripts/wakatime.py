from rauth import OAuth2Service
from urllib.parse import parse_qsl
import hashlib
import os


class WakatimeAPI:
    session = None
    authorize_url = "https://wakatime.com/oauth/authorize"
    access_token_url = "https://wakatime.com/oauth/token"
    base_url = "https://wakatime.com/api/v1/"
    redirect_uri = "https://wakatime.com/oauth/test"
    headers = {"Accept": "application/x-www-form-urlencoded"}

    def __init__(self, client_id, client_secret):
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

    def get_url_auth(self):
        params = {
            "scope": "email,read_stats",
            "response_type": "code",
            "state": self.state,
            "redirect_uri": self.redirect_uri,
        }

        url = self.service.get_authorize_url(**params)

        return url

    def set_auth_session(self, code):
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

    def refresh_session(self):
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

    def _new_refresh_session(self, refresh_token):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        self.session = self.service.get_auth_session(data=data)

    def get_refresh_token(self):
        return dict(parse_qsl(self.session.access_token_response.text))["refresh_token"]

    def get_access_token(self):
        return dict(parse_qsl(self.session.access_token_response.text))["access_token"]


class WakatimeStats(WakatimeAPI):
    def __init__(self, client_id, client_secret):
        super(WakatimeStats, self).__init__(client_id, client_secret)

    def get_stats(self):
        return self.session.get("users/current/stats").json()

    @staticmethod
    def new_refresh_session(refresh):
        def wrapper(self, refresh_token):
            self._new_refresh_session(refresh_token)
            return refresh(self, refresh_token)

        return wrapper

    @new_refresh_session
    async def get_lang_stats(self, refresh_token):
        """Статистика по языкам"""

        return self.get_stats()["data"]["languages"]

    @new_refresh_session
    async def get_all_time(self, refresh_token):
        return self.get_stats()["data"]["human_readable_total_including_other_language"]

    @new_refresh_session
    async def get_os_stats(self, refresh_token):
        return self.get_stats()["data"]["operating_systems"]

    @new_refresh_session
    async def get_editors_stats(self, refresh_token):
        return self.get_stats()["data"]["editors"]

    @new_refresh_session
    async def get_categories_stats(self, refresh_token):
        return self.get_stats()["data"]["categories"]
