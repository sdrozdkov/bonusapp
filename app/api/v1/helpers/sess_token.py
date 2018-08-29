import secrets
import string
from app import redis_client


class SessToken:

    def __init__(self):
        self._value = self._generate()

    def _generate(self):
        alphabet = string.digits + string.ascii_letters
        return ''.join(secrets.choice(alphabet) for i in range(50))

    def save(self):
        redis_client.hset('sess_token', self.value)

    @property
    def value(self):
        return self._value
