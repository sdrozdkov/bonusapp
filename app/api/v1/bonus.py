import logging
from flask import jsonify, request
from app.models.bonus_card import BonusCardTrx, BonusCard
from app.decorators.auth import api_auth

logger = logging.getLogger(__name__)


@api_auth()
def post_bonus_trx():
    """
     POST Bonus transaction
     ---
    responses:
      200:
        description: Return 200 OK if trx created
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

    bonus_card.card_history.append(bonus_trx)
    bonus_card.save()

    return jsonify({"result": {"message": "ok"}}), 200
