import logging
from flask import jsonify, g, redirect, url_for
from app.decorators.auth import check_authentication
from app.models.user import User
from app.models.bonus_card import BonusCard

logger = logging.getLogger(__name__)


@check_authentication()
def get_profile():
    """
     GET Demo API
     ---
    responses:
      200:
        description: Returns GET demo api response
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
     POST Demo API
     ---
    responses:
      200:
        description: Returns POST demo api response
    """
    user = User.objects(id=g.user_info['user_id']).first()

    if not user.bonus_card.card_history:
        return jsonify({"result": {"message": "No any bonus transaction"}}), 404

    # print(user.bonus_card.card_history)
    # print(user.bonus_card.card_history.to_json())
    # print(user.bonus_card.card_history)
    return jsonify({
        "result":
        {"transactions": [{"trx_id": trx.trx_id,
                           "trx_value": trx.trx_value,
                           "departure_airport": trx.departure_airport,
                           "arrival_airport": trx.arrival_airport,
                           "flight_date": trx.flight_date} for trx in user.bonus_card.card_history]}
    }), 200


def create_example_users():

    User(email='s.drozdkov@yandex.ru', full_name='Sergey Drozdkov',
         bonus_card=BonusCard(bonus_card_number='111').save()).save()
    User(email='ssdrozdkov2@example.com', full_name='Sergey Drozdkov',
         bonus_card=BonusCard(bonus_card_number='222').save()).save()
    User(email='ssdrozdkov3@example.com', full_name='Sergey Drozdkov',
         bonus_card=BonusCard(bonus_card_number='333').save()).save()
    User(email='ssdrozdkov4@example.com', full_name='Sergey Drozdkov',
         bonus_card=BonusCard(bonus_card_number='444').save()).save()
    User(email='ssdrozdkov5@example.com', full_name='Sergey Drozdkov',
         bonus_card=BonusCard(bonus_card_number='555').save()).save()

    return jsonify({"result": {"message": "created"}}), 200
