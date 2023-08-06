'''
Response: {
    user_id: str,
    email: str or None,
    name: str,
    surname: str or None,
    back_url: str of None
} or {} if error occured
'''

import os
import logging
from pprint import pformat

import aiohttp
from yarl import URL
from aiohttp.web import HTTPFound

from .cfg import cfg

HOST_PATH = os.environ.get("AIOHTTP_LOGIN_HOST_PATH")

log = logging.getLogger(__name__)


async def vkontakte(request):
    if 'error' in request.query:
        return {}

    if HOST_PATH:
        url = HOST_PATH + str(request.rel_url.with_query(None))
    else:
        url = str(request.url.with_query(None))

    common_params = {
        'client_id': cfg.VKONTAKTE_ID,
        'redirect_uri': url,
        'v': '5.60',
    }

    # Step 1: redirect browser to login dialog
    if 'code' not in request.query:
        url = 'http://api.vk.com/oauth/authorize'
        params = common_params.copy()
        params['scope'] = 'email'
        if cfg.BACK_URL_QS_KEY in request.query:
            params['state'] = request.query[cfg.BACK_URL_QS_KEY]
        raise HTTPFound(URL(url).with_query(params))

    # Step 2: get access token
    url = 'https://oauth.vk.com/access_token'
    params = common_params.copy()
    params.update({
        'client_secret': cfg.VKONTAKTE_SECRET,
        'code': request.query['code'],
    })
    async with aiohttp.ClientSession(loop=request.app.loop) as client:
        async with client.get(URL(url).with_query(params)) as resp:
            data = await resp.json()
        if 'user_id' not in data:
            log.error('Vkontakte: no user_id in data: %s', data)
            return {}

        # get user profile
        url = URL('https://api.vk.com/method/users.get').with_query(
            access_token=data['access_token'],
            uid=data['user_id'],
            fields='nickname,screen_name',
            v='5.60'
        )
        async with client.get(url) as resp:
            profile = await resp.json()

    log.debug('VK profile: %s', pformat(profile))

    assert 'response' in profile, profile
    profile = profile['response'][0]
    log.debug('vk profile: %s', pformat(profile))
    name = profile.get('first_name')
    if not name and 'email' in data:
        name = data['email'].split('@')[0]
    if not name:
        name = str(data['user_id'])
    return {
        'user_id': str(data['user_id']),
        'email': data.get('email'),
        'name': name,
        'surname': data.get('last_name'),
        'back_to': request.query.get('state'),
    }


async def google(request):
    if 'error' in request.query:
        return {}

    if HOST_PATH:
        url = HOST_PATH + str(request.rel_url.with_query(None))
    else:
        url = str(request.url.with_query(None))

    common_params = {
        'client_id': cfg.GOOGLE_ID,
        'redirect_uri': url,
    }

    # Step 1: redirect to get code
    if 'code' not in request.query:
        url = 'https://accounts.google.com/o/oauth2/auth'
        params = common_params.copy()
        params.update({
            'response_type': 'code',
            'scope': ('https://www.googleapis.com/auth/userinfo.profile'
                      ' https://www.googleapis.com/auth/userinfo.email'),
        })
        if cfg.BACK_URL_QS_KEY in request.query:
            params['state'] = request.query[cfg.BACK_URL_QS_KEY]
        url = URL(url).with_query(params)
        raise HTTPFound(url)

    # Step 2: get access token
    url = 'https://accounts.google.com/o/oauth2/token'
    params = common_params.copy()
    params.update({
        'client_secret': cfg.GOOGLE_SECRET,
        'code': request.query['code'],
        'grant_type': 'authorization_code',
    })
    async with aiohttp.ClientSession(loop=request.app.loop) as client:
        async with client.post(url, data=params) as resp:
            data = await resp.json()
        assert 'access_token' in data, data
        log.debug('data: %s', pformat(data))

        # get user profile
        headers = {'Authorization': 'Bearer ' + data['access_token']}
        url = "https://www.googleapis.com/oauth2/v1/userinfo"
        async with client.get(url, headers=headers) as resp:
            profile = await resp.json()

    log.debug('google profile: %s', pformat(profile))

    email = profile["email"]
    name = profile.get('given_name', "anonymous")
    surname = profile.get("family_name")
    if not name:
        if email:
            name = email.split('@')[0]
        else:
            name = str(data['id'])
    return {
        'user_id': profile['id'],
        'email': email,
        'name': name,
        'surname': surname,
        'back_to': request.query.get('state'),
    }


async def facebook(request):
    if 'error' in request.query:
        return {}

    if HOST_PATH:
        url = HOST_PATH + str(request.rel_url.with_query(None))
    else:
        url = str(request.url.with_query(None))

    common_params = {
        'client_id': cfg.FACEBOOK_ID,
        'redirect_uri': url,
    }

    # Step 1: redirect to get code
    if 'code' not in request.query:
        params = common_params.copy()
        params.update({
            'response_type': 'code',
            'scope': 'email',
        })
        if cfg.BACK_URL_QS_KEY in request.query:
            params['state'] = request.query[cfg.BACK_URL_QS_KEY]
        url = URL(
            'https://www.facebook.com/v2.8/dialog/oauth').with_query(params)
        raise HTTPFound(url)

    # Step 2: get access token
    url = URL('https://graph.facebook.com/v2.8/oauth/access_token').with_query(
        dict(
            common_params,
            client_secret=cfg.FACEBOOK_SECRET,
            code=request.query['code'],
        ))
    async with aiohttp.ClientSession(loop=request.app.loop) as client:
        async with client.get(url) as resp:
            data = await resp.json()
        assert 'access_token' in data, data

        # get profile
        url = URL('https://graph.facebook.com/v2.8/me').with_query(
            fields='id,email,first_name',
            access_token=data['access_token'])
        async with client.get(url) as resp:
            profile = await resp.json()
        log.debug('facebook profile: %s', pformat(profile))

    email = profile.get('email')
    name = profile.get('first_name')
    if not name:
        if email:
            name = email.split('@')[0]
        else:
            name = str(profile['id'])

    return {
        'user_id': profile['id'],
        'email': email,
        'name': name,
        'surname': profile.get("last_name"),
        'back_to': request.query.get('state'),
    }
