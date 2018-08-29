import mongoengine as mge


class BonusCardTrx(mge.EmbeddedDocument):
    trx_id = mge.StringField(required=True)  # номер транзакции
    trx_value = mge.IntField(required=True)  # Сколько начислено бонусных единиц(миль)
    departure_airport = mge.StringField(required=True)  # откуда
    arrival_airport = mge.StringField(required=True)  # куда
    flight_date = mge.DateTimeField(required=True)  # дата полёта


class BonusCard(mge.Document):
    bonus_card_number = mge.StringField(min_length=3, max_length=10, unique=True, required=True)
    balance = mge.IntField(min_value=0, default=0)
    card_history = mge.ListField(mge.EmbeddedDocumentField(BonusCardTrx))

    meta = {'allow_inheritance': True}
