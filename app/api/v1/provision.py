import logging
from flask import jsonify
from app.models.user import User
from app.models.bonus_card import BonusCard

logger = logging.getLogger(__name__)


def create_example_users():

    # Specify your test users before start
    User(
        email='bundieboss@gmail.com',
        full_name='Sergey Drozdkov',
        bonus_card=BonusCard(bonus_card_number='111').save()
    ).save()

    User(
        email='example2@example.com',
        full_name='Ivan Ivanov',
        bonus_card=BonusCard(bonus_card_number='222').save()
    ).save()

    User(
        email='example3@example.com',
        full_name='Petr Petrov',
        bonus_card=BonusCard(bonus_card_number='333').save()
    ).save()

    User(
        email='example4@example.com',
        full_name='Olga Olgova',
        bonus_card=BonusCard(bonus_card_number='444').save()
    ).save()

    User(
        email='example5@example.com',
        full_name='User Userov',
        bonus_card=BonusCard(bonus_card_number='555').save()
    ).save()

    return jsonify({"result": {"message": "users created"}}), 200
