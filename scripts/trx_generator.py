import json
import requests
import datetime
import secrets
import string
from random import randint

TRX_ENDPOINT = 'http://localhost:8080/api/v1/bonus'
API_KEY = "6a203a7c98d05eb4f390e683353a16485f2b7379470def0a9ef07e14a376c8b6"
BONUS_CARD_NUMBER = '111'


trx_ids = [i for i in range(100, 203, 1)]

for trx_id in trx_ids:
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=randint(24, 480))
    date = now + delta

    alphabet = string.ascii_uppercase

    crafted = {
        "bonus_card_number": BONUS_CARD_NUMBER,
        "trx_value": randint(1, 100),
        "departure_airport": ''.join(secrets.choice(alphabet) for i in range(3)),
        "arrival_airport": ''.join(secrets.choice(alphabet) for i in range(3)),
        "flight_date": f"{date}",
        "trx_id": str(trx_id)
    }

    r = requests.post(
        url=TRX_ENDPOINT,
        headers={'Content-Type': 'application/json', 'Authorization': API_KEY},
        data=json.dumps(crafted)
    )
