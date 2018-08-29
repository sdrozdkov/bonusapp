from flask import Blueprint
from app.api.v1.auth import post_email_auth, validate_auth_code
from app.api.v1.profile import get_profile, get_bonus_history
from app.api.v1.bonus import post_bonus_trx

api_v1 = Blueprint('api.v1', __name__)

api_v1.add_url_rule('/auth', view_func=post_email_auth, methods=['POST'])

api_v1.add_url_rule('/auth/validate', view_func=validate_auth_code, methods=['POST'])

api_v1.add_url_rule('/profile', view_func=get_profile, methods=['GET'])
api_v1.add_url_rule('/profile/history', view_func=get_bonus_history, methods=['GET'])
api_v1.add_url_rule('/profile/history', view_func=get_bonus_history, methods=['GET'])
api_v1.add_url_rule('/bonus', view_func=post_bonus_trx, methods=['POST'])
