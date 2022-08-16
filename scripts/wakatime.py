from hashlib import sha1
from os import urandom
from rauth import OAuth2Service
from datetime import datetime as dt
from scripts.Auth_Wakatime import sign_up
from json import loads
from os import getenv


async def wakatime_stats(email, password):

    service = OAuth2Service(
        client_id=getenv("CLIENT_ID"),
        client_secret=getenv("SECRET"),
        name='wakatime',
        authorize_url='https://wakatime.com/oauth/authorize',
        access_token_url='https://wakatime.com/oauth/token',
        base_url='https://wakatime.com/api/v1/')

    redirect_uri = 'https://wakatime.com/oauth/test'
    state = sha1(urandom(40)).hexdigest()
    params = {'scope': 'email,read_stats',
              'response_type': 'code',
              'state': state,
              'redirect_uri': redirect_uri}

    url = service.get_authorize_url(**params)

    code = await sign_up(url, email, password)

    headers = {'Accept': 'application/x-www-form-urlencoded'}
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] wakatime_stats: Getting an access token...')
    session = service.get_auth_session(headers=headers,
                                       data={'code': code,
                                             'grant_type': 'authorization_code',
                                             'redirect_uri': redirect_uri})

    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] wakatime_stats: Getting current user from API...')
    user = session.get('users/current').json()
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] wakatime_stats: Authenticated via OAuth as {0}'.format(user['data']['email']))
    print(f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] wakatime_stats: Getting user\'s coding stats from API...')
    stats = session.get('users/current/stats')
    return loads(stats.text)
