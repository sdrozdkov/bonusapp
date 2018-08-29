import mongoengine as mge
from app.models.bonus_card import BonusCard


class User(mge.Document):
    email = mge.StringField(max_length=255, unique=True, required=True)
    full_name = mge.StringField(max_length=100, required=True)
    bonus_card = mge.ReferenceField(BonusCard)

    meta = {'allow_inheritance': True}
