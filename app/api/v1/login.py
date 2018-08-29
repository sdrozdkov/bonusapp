import logging
import datetime
from flask import jsonify, request, make_response, redirect, url_for, session
from app.tasks import auth_code_task
from app.api.v1.helpers.sess_token import SessToken
from app import redis_client
from app.models.user import User

logger = logging.getLogger(__name__)


def post_email_auth():
    """
     POST Demo API
     ---
    responses:
      200:
        description: schedule task for sending auth code to user's email
    """
    content = request.get_json()

    # TODO: implement validation data
    email = content.get('email')
    if not email or email is None:
        return jsonify({"result": {"message": "no email provided"}}), 400

    # get user_id from mongo
    # if user_id is None: return 404
    user = User.objects(email=email).first()
    if user is None:
        return jsonify({"result": {"message": "not found"}}), 404

    ttl = 300  # 5 minutes

    sess_token = SessToken()

    resp = make_response(jsonify({"result": {"message": "ok"}}), 200)
    redis_client.set(name=f'sess_token_{sess_token.value}', value=user.id, ex=ttl)
    resp.set_cookie('sess_token', sess_token.value, max_age=ttl)

    auth_code_task.delay(email, sess_token.value)

    return resp


def validate_auth_code():
    """
     POST Auth code validation
     ---
    responses:
      200:
        description: Returns result of code verification
    """
    sess_token = request.cookies.get('sess_token')
    if not sess_token or sess_token is None:
        return redirect(url_for('api.v1.post_email_auth'), code=302)

    content = request.get_json()

    auth_code = content.get('code')
    if not auth_code or auth_code is None:
        return jsonify({"result": {"message": "no code provided"}}), 400

    if auth_code != redis_client.get(f'authcode_{sess_token}'):
        return jsonify({"result": {"message": "wrong code"}}), 400

    resp = make_response(jsonify({"result": {"message": "ok"}}), 200)
    user_id = redis_client.get(f'sess_token_{sess_token}')

    ttl = 60 * 60 * 24 * 31  # 31 days

    sess_id = SessToken()

    redis_client.set(name=f'sessid_{sess_id.value}', value=user_id, ex=ttl)
    redis_client.delete(f'authcode_{sess_token}')
    redis_client.delete(f'sess_token_{sess_token}')

    session['sessid'] = sess_id.value

    return resp
