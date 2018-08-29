import json
import logging
import secrets
import string
from app import celery_app, current_config, mail, redis_client
from .base import BaseTask
from flask_mail import Message


logger = logging.getLogger(__name__)


class Task1(object):

    def run(self, *args, **kwargs):
        print("this is task 1")


class AuthCode:

    def __init__(self):
        self._auth_code = self._generate()

    def _generate(self) -> str:
        alphabet = string.digits
        return ''.join(secrets.choice(alphabet) for i in range(4))

    def save(self, session_token: str):
        redis_client.set(name=f'authcode_{session_token}', value=f'{self._auth_code}')

    def send(self, email: str):
        mail_subject = "BonusApp Auth Code"

        mail_body = f"Your auth code: {self._auth_code}"
        msg = Message(subject=mail_subject,
                      body=mail_body,
                      sender=current_config.DEFAULT_MAIL_SENDER,
                      recipients=[email])
        mail.send(msg)


@celery_app.task(bind=True, base=BaseTask, name='task_1')
def task_1(*args, **kwargs):
    Task1().run(*args, **kwargs)


@celery_app.task(bind=True, base=BaseTask, name='auth_code_task')
def auth_code_task(self, email, session_token):
    ctx = AuthCode()

    ctx.save(session_token)

    ctx.send(email)
