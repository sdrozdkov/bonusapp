import logging
from flask import jsonify, g, redirect, url_for, request
from app.decorators.auth import check_authentication
from app.models.user import User
from app.models.bonus_card import BonusCard

logger = logging.getLogger(__name__)


@check_authentication()
def get_profile():
    """
     GET User profile
     ---
    responses:
      200:
        description: Returns user profile
    """
    user = User.objects(id=g.user_info['user_id']).first()

    return jsonify({"result": {
        "email": user.email,
        "full_name": user.full_name,
        "bonus_card": user.bonus_card.bonus_card_number,
    }}), 200


@check_authentication()
def get_bonus_history():
    """
     GET Personilized bonus history
     ---
    responses:
      200:
        description: Returns history with pagination
    """
    raw_page = request.args.get('page', 1, type=int)
    if raw_page < 0:
        raw_page = 1

    page = raw_page - 1

    pagesize = 10

    user = User.objects(id=g.user_info['user_id']).first()

    if not user.bonus_card.card_history:
        return jsonify({"result": {"message": "No any bonus transaction"}}), 404

    trx_history = user.bonus_card.card_history

    total_pages = len(trx_history) // pagesize
    if len(trx_history) % pagesize > 0:
        total_pages += 1

    if raw_page > total_pages:
        return jsonify({"result": {"message": "Wrong page number"}}), 404

    coursor = page * pagesize
    limit = coursor + pagesize

    return jsonify({
        "result":
        {
            "page": raw_page,
            "total_pages": int(total_pages),
            "transactions": [{"trx_id": trx.trx_id,
                              "trx_value": trx.trx_value,
                              "departure_airport": trx.departure_airport,
                              "arrival_airport": trx.arrival_airport,
                              "flight_date": trx.flight_date} for trx in trx_history[coursor:limit]],
        }
    }), 200
