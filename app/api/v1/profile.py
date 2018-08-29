import logging
from flask import jsonify

logger = logging.getLogger(__name__)


def get_profile():
    """
     GET Demo API
     ---
    responses:
      200:
        description: Returns GET demo api response
    """
    logger.debug("in demo api")
    return jsonify({'message': "demo get api"}), 200


def get_bonus_history():
    """
     POST Demo API
     ---
    responses:
      200:
        description: Returns POST demo api response
    """
    return jsonify({'name': "demo post api"}), 200
