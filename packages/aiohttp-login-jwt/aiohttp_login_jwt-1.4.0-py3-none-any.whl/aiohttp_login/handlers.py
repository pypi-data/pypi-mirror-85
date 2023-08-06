import os
import re
import logging

from aiohttp import web

from aiohttp_jinja2 import render_template

from .cfg import cfg
from . import forms
from . import oauth
from . import flash
from .decorators import login_required
from .utils import (encrypt_password, make_confirmation_link,
                    check_password, is_confirmation_allowed,
                    get_random_string, url_for, get_client_ip, redirect,
                    render_and_send_mail, is_confirmation_expired, themed,
                    common_themed, social_url, authorize_user, api_call_count_cache)

import jwt

JWT_SECRET = os.environ.get('JWT_SECRET', 'secret')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXP_DELTA_SECONDS = int(os.environ.get('JWT_EXP_DELTA_SECONDS', 60 * 20))

log = logging.getLogger(__name__)


async def social(request):
    provider = request.match_info['provider']
    data = await getattr(oauth, provider)(request)
    log.info(str(data))
    db = cfg.STORAGE

    user = None
    while 'user_id' in data:
        # try to find user by provider_id
        user = await db.get_user({provider: data['user_id']})
        if user:
            break

        if data['email']:
            # try to find user by email
            user = await db.get_user({'email': data['email']})
            log.info(str(user))
            if user:
                await db.update_user(user, {provider: data['user_id']})
                break

            # register new user
            password = get_random_string(*cfg.PASSWORD_LEN)
            user = await db.create_user({
                'name': data['name'],
                'surname': data['surname'],
                'email': data['email'],
                'password': encrypt_password(password),
                'status': 'active',
                'created_ip': get_client_ip(request),
                'role': "registered",
                provider: data['user_id'],
            })
            break
        break

    if user:
        jwt_token = await authorize_user(request, user)
        flash.success(request, cfg.MSG_LOGGED_IN)
        url = data['back_to'] or cfg.LOGIN_REDIRECT

        # if provider in ['google', 'facebook']:
        #    return render_template(
        #        common_themed('http_redirect.html'),
        #        request, {'url': url, 'auth': {'cfg': cfg}})

        redirect_v = redirect(url)
        redirect_v.set_cookie(name="jwt", value="%s" % jwt_token.decode('utf-8'))
        return redirect_v

    flash.error(request, cfg.MSG_AUTH_FAILED)
    return redirect('auth_login')


async def registration(request):
    form = await forms.get('Registration').init(request)
    db = cfg.STORAGE

    while request.method == 'POST' and await form.validate():

        user = await db.create_user({
            'name': form.name.data,
            'email': form.email.data,
            'password': encrypt_password(form.password.data),
            'surname': form.surname.data,
            'company': form.company.data,
            'status': ('confirmation' if cfg.REGISTRATION_CONFIRMATION_REQUIRED
                       else 'active'),
            'created_ip': get_client_ip(request),
            'role': 'registered'
        })

        if not cfg.REGISTRATION_CONFIRMATION_REQUIRED:
            jwt_token = await authorize_user(request, user)
            flash.success(request, cfg.MSG_LOGGED_IN)
            redirect_v = redirect(cfg.LOGIN_REDIRECT)
            redirect_v.set_cookie(name="jwt", value="%s" % jwt_token.decode('utf-8'))
            return redirect_v

        confirmation = await db.create_confirmation(user, 'registration')
        link = await make_confirmation_link(request, confirmation)
        try:
            await render_and_send_mail(
                request, form.email.data,
                common_themed('registration_email.html'), {
                    'auth': {
                        'cfg': cfg,
                    },
                    'host': request.host,
                    'link': link,
                })
        except Exception as e:
            log.error('Can not send email', exc_info=e)
            form.email.errors.append(cfg.MSG_CANT_SEND_MAIL)
            await db.delete_confirmation(confirmation)
            await db.delete_user(user)
            break
        return redirect('auth_registration_requested')

    return render_template(themed('registration.html'), request, {
        'auth': {
            'url_for': url_for,
            'cfg': cfg,
            'form': form,
            'social_url': social_url(request),
        }
    })


async def login(request):
    form = await forms.get('Login').init(request)

    while request.method == 'POST' and form.validate():

        user = await cfg.STORAGE.get_user({'email': form.email.data})
        if not user:
            form.email.errors.append(cfg.MSG_UNKNOWN_EMAIL)
            break

        if not check_password(form.password.data, user['password']):
            form.password.errors.append(cfg.MSG_WRONG_PASSWORD)
            break

        if user['status'] == 'banned':
            form.email.errors.append(cfg.MSG_USER_BANNED)
            break
        if user['status'] == 'confirmation':
            form.email.errors.append(cfg.MSG_ACTIVATION_REQUIRED)
            break
        assert user['status'] == 'active'

        jwt_token = await authorize_user(request, user)
        """ JWT generating """

        try:
            url = request.cookies['req_url']
        except Exception as exc:
            print("req_url does not exists! Exception: {exc}".format(exc=str(exc)))
            url = request.query.get(cfg.BACK_URL_QS_KEY, cfg.LOGIN_REDIRECT)

        redirect_v = redirect(url)
        redirect_v.set_cookie(name="jwt", value="%s" % jwt_token.decode('utf-8'))
        flash.success(request, cfg.MSG_LOGGED_IN)

        return redirect_v

    return render_template(themed('login.html'), request, {
        'auth': {
            'url_for': url_for,
            'cfg': cfg,
            'form': form,
            'social_url': social_url(request),
        }
    })


async def verify_token(request):
    token = request.cookies.get('jwt')
    req_url = request.cookies.get('req_url')

    try:
        decoded = jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])
    except Exception as e:
        log.error('Token verification failed', exc_info=e)
        return web.json_response({'is_valid': False,
                                  'status_code': 401,
                                  'err_msg': e.__repr__()})

    role = decoded.get('role', "")
    black_list = cfg.ROLES_API_BLACK_LIST.get(role)
    if black_list:
        if any([re.compile(bl_item).search(req_url) for bl_item in black_list]):
            log.info('Requested URL is forbidden for user %s' % str(decoded.get("username")))
            return web.json_response({'is_valid': False,
                                      'status_code': 403})

    log.info('Token verified for user: %s' % str(decoded["username"]))
    return web.json_response({'is_valid': True,
                              'role': role})


async def logout(request):
    # session = await get_session(request)
    # session.pop(cfg.SESSION_USER_KEY, None)
    redirect_v = redirect(cfg.LOGOUT_REDIRECT)
    redirect_v.set_cookie(name="jwt", value="")
    flash.info(request, cfg.MSG_LOGGED_OUT)

    return redirect_v


async def reset_password(request):
    db = cfg.STORAGE
    form = await forms.get('ResetPasswordRequest').init(request)

    while request.method == 'POST' and form.validate():
        user = await db.get_user({'email': form.email.data})
        if not user:
            form.email.errors.append(cfg.MSG_UNKNOWN_EMAIL)
            break

        if user['status'] == 'banned':
            form.email.errors.append(cfg.MSG_USER_BANNED)
            break
        if user['status'] == 'confirmation':
            form.email.errors.append(cfg.MSG_ACTIVATION_REQUIRED)
            break
        assert user['status'] == 'active'

        if not await is_confirmation_allowed(user, 'reset_password'):
            form.email.errors.append(cfg.MSG_OFTEN_RESET_PASSWORD)
            break

        confirmation = await db.create_confirmation(user, 'reset_password')
        link = await make_confirmation_link(request, confirmation)
        try:
            await render_and_send_mail(
                request, form.email.data,
                common_themed('reset_password_email.html'), {
                    'auth': {
                        'cfg': cfg,
                    },
                    'host': request.host,
                    'link': link,
                })
        except Exception as e:
            log.error('Can not send email', exc_info=e)
            form.email.errors.append(cfg.MSG_CANT_SEND_MAIL)
            await db.delete_confirmation(confirmation)
            break

        return redirect('auth_reset_password_requested')

    return render_template(themed('reset_password.html'), request, {
        'auth': {
            'url_for': url_for,
            'cfg': cfg,
            'form': form,
        }
    })


async def reset_password_allowed(request, confirmation):
    db = cfg.STORAGE
    form = await forms.get('ResetPassword').init(request)
    user = await db.get_user({'id': confirmation['user_id']})
    assert user

    while request.method == 'POST' and form.validate():
        await db.update_user(
            user, {'password': encrypt_password(form.password.data)})
        await db.delete_confirmation(confirmation)
        jwt_token = await authorize_user(request, user)

        redirect_v = redirect(cfg.LOGIN_REDIRECT)
        redirect_v.set_cookie(name="jwt", value="%s" % jwt_token.decode('utf-8'))

        flash.success(request, cfg.MSG_PASSWORD_CHANGED)
        flash.success(request, cfg.MSG_LOGGED_IN)

        return redirect_v

    return render_template(themed('reset_password_allowed.html'), request, {
        'auth': {
            'url_for': url_for,
            'cfg': cfg,
            'form': form,
        }
    })


@login_required
async def change_email(request):
    db = cfg.STORAGE
    user = request[cfg.REQUEST_USER_KEY]
    form = await forms.get('ChangeEmail').init(
        request, email=user['email'])

    while request.method == 'POST' and form.validate(user['email']):
        confirmation = await db.get_confirmation(
            {'user': user, 'action': 'change_email'})
        if confirmation:
            await db.delete_confirmation(confirmation)

        confirmation = await db.create_confirmation(
            user, 'change_email', form.email.data)
        link = await make_confirmation_link(request, confirmation)
        try:
            await render_and_send_mail(
                request, form.email.data,
                common_themed('change_email_email.html'), {
                    'auth': {
                        'cfg': cfg,
                    },
                    'host': request.host,
                    'link': link,
                })
        except Exception as e:
            log.error('Can not send email', exc_info=e)
            form.email.errors.append(cfg.MSG_CANT_SEND_MAIL)
            await db.delete_confirmation(confirmation)
            break

        flash.success(request, cfg.MSG_CHANGE_EMAIL_REQUESTED)
        return redirect(request.path)

    return render_template(themed('change_email.html'), request, {
        'auth': {
            'cfg': cfg,
            'form': form
        }
    })


@login_required
async def change_password(request):
    db = cfg.STORAGE
    user = request[cfg.REQUEST_USER_KEY]
    form = await forms.get('ChangePassword').init(request)

    while request.method == 'POST' and form.validate():
        if not check_password(form.cur_password.data, user['password']):
            form.cur_password.errors.append(cfg.MSG_WRONG_PASSWORD)
            break

        password = encrypt_password(form.new_password.data)
        await db.update_user(user, {'password': password})

        flash.success(request, cfg.MSG_PASSWORD_CHANGED)
        return redirect(request.path)

    return render_template(themed('change_password.html'), request, {
        'auth': {
            'cfg': cfg,
            'form': form,
            'url_for': url_for,
        }
    })


async def confirmation(request):
    db = cfg.STORAGE
    code = request.match_info['code']

    confirmation = await db.get_confirmation({'code': code})
    if confirmation and is_confirmation_expired(confirmation):
        await db.delete_confirmation(confirmation)
        confirmation = None

    if confirmation:
        action = confirmation['action']

        if action == 'registration':
            user = await db.get_user({'id': confirmation['user_id']})
            await db.update_user(user, {'status': 'active'})
            jwt_token = await authorize_user(request, user)
            redirect_v = redirect(cfg.LOGIN_REDIRECT)
            redirect_v.set_cookie(name="jwt", value="%s" % jwt_token.decode('utf-8'))
            await db.delete_confirmation(confirmation)
            flash.success(request, cfg.MSG_ACTIVATED)
            flash.success(request, cfg.MSG_LOGGED_IN)
            return redirect_v

        if action == 'reset_password':
            return await reset_password_allowed(request, confirmation)

        if action == 'change_email':
            user = await db.get_user({'id': confirmation['user_id']})
            await db.update_user(user, {'email': confirmation['data']})
            await db.delete_confirmation(confirmation)
            flash.success(request, cfg.MSG_EMAIL_CHANGED)
            return redirect('auth_change_email')

    return render_template(themed('confirmation_error.html'), request, {
        'auth': {
            'cfg': cfg
        }
    })


def template_handler(template, context=None):
    async def handler(request):
        return render_template(themed(template), request, context)

    return handler


async def check_call_limits(request):
    token = request.cookies.get('jwt')
    req_url = request.cookies.get('req_url')

    try:
        decoded = jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])
    except Exception as e:
        log.error('Token verification failed', exc_info=e)
        return web.json_response({'allowed': False,
                                  'status_code': 401,
                                  'err_msg': e.__repr__()})

    role = decoded.get('role', "")

    if cfg.CACHE:
        count = api_call_count_cache(cfg.CACHE, str(decoded["user_id"])+str(req_url))
    else:
        return web.json_response({"allowed": True,
                                  "status_code": 200})

    limits = cfg.ROLES_API_LIMITS.get(role)
    if limits:
        api_limit = limits.get(req_url)
    else:
        return web.json_response({"allowed": True,
                                  "status_code": 200})
    if api_limit:
        if count > api_limit:
            return web.json_response({"allowed": False,
                                      "status_code": 403})
        else:
            return web.json_response({"allowed": True,
                                      "status_code": 200})
    else:
        return web.json_response({"allowed": True,
                                  "status_code": 200})
