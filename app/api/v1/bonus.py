import logging
import json
from flask import jsonify, request
from app.models.bonus_card import BonusCardTrx, BonusCard
import mongoengine

logger = logging.getLogger(__name__)


def post_bonus_trx():
    """
     POST Demo API
     ---
    responses:
      200:
        description: Returns POST demo api response
    """
    content = request.get_json()

    bonus_card_number = content.get('bonus_card_number')
    bonus_card = BonusCard.objects(bonus_card_number=bonus_card_number).first()

    bonus_trx = BonusCardTrx(
        trx_id=content.get('trx_id'),
        trx_value=content.get('trx_value'),
        departure_airport=content.get('departure_airport'),
        arrival_airport=content.get('arrival_airport'),
        flight_date=content.get('flight_date'),
    )

    print(bonus_card.to_json())

    bonus_card.card_history.append(bonus_trx)
    bonus_card.save()

    # TODO: implement validation data

    return jsonify({'name': "demo post api"}), 200
