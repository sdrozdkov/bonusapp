import logging
from flask import jsonify, request, make_response
from app.tasks import auth_code_task
from app.api.v1.helpers.sess_token import SessToken
from app import redis_client

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
    user_id = '1'

    sess_token = SessToken()

    resp = make_response(jsonify({"result": {"message": "ok"}}), 200)
    resp.set_cookie('sess_token', sess_token.value)
    redis_client.hset('sess_token_', sess_token.value, user_id)
    redis_client.set(name=f'sess_token_{sess_token.value}', value=f'"{user_id}"')

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
    content = request.get_json()
    print(content)

    return jsonify({"result": {"message": "ok"}}), 200
