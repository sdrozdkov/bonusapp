import logging
from flask import jsonify

logger = logging.getLogger(__name__)


def post_bonus_trx():
    """
     POST Demo API
     ---
    responses:
      200:
        description: Returns POST demo api response
    """
    return jsonify({'name': "demo post api"}), 200
