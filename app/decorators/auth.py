import json
import logging
import requests
import datetime
from functools import wraps
from flask import current_app, g, jsonify, session, request, redirect, url_for
from app import redis_client

logger = logging.getLogger(__name__)


def check_authentication():
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger.debug("in auth decorator")
            if current_app.config['IS_AUTH_ENABLED']:
                sess_id = session.get('sessid')
                if not sess_id or sess_id is None:
                    return redirect(url_for('api.v1.post_email_auth', next=request.url))

                user_id = redis_client.get(f'sessid_{sess_id}')
                if not user_id or user_id is None:
                    return redirect(url_for('api.v1.post_email_auth', next=request.url))

                logger.debug("AUTH is ENABLED")
                user_info = {"user_id": user_id}
                g.user_info = user_info
                logger.info(
                    f"REMOTE_ADDR: {request.remote_addr} METHOD: {request.method} URL: {request.url} USER_ID: {user_info['user_id']} \nDATA: {request.data}"
                )
            else:
                logger.debug("AUTH is DISABLED")
                logger.info("REMOTE_ADDR: {} METHOD: {} URL: {} \nDATA: {}".format(request.remote_addr, request.method,
                                                                                   request.url, request.data))

            return f()
        return decorated_function

    return login_required


# # Authentication objects for username/password auth, token auth, and a
# # token optional auth that is used for open endpoints.
# basic_auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth('Bearer')
# token_optional_auth = HTTPTokenAuth('Bearer')
#
#
# @basic_auth.verify_password
# def verify_password(nickname, password):
#     """Password verification callback."""
#     if not nickname or not password:
#         return False
#     return True
#
#
# @basic_auth.error_handler
# def password_error():
#     """Return a 401 error to the client."""
#     # To avoid login prompts in the browser, use the "Bearer" realm.
#     return (jsonify({'error': 'authentication required'}), 401,
#             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})
#
#
# @token_auth.verify_token
# def verify_token(token, add_to_session=False):
#     """Token verification callback."""
#     if add_to_session:
#         # clear the session in case auth fails
#         if 'nickname' in session:
#             del session['nickname']
#     return True
#
#
# @token_auth.error_handler
# def token_error():
#     """Return a 401 error to the client."""
#     return (jsonify({'error': 'authentication required'}), 401,
#             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})
#
#
# @token_optional_auth.verify_token
# def verify_optional_token(token):
#     """Alternative token authentication that allows anonymous logins."""
#     if token == '':
#         # no token provided, mark the logged in users as None and continue
#         g.current_user = None
#         return True
#     # but if a token was provided, make sure it is valid
#     return verify_token(token)
