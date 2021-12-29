import base64
import calendar
import hashlib
import hmac
from datetime import datetime, timedelta
from flask import current_app
from jwt import jwt

from project.config import BaseConfig


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def get_hash(password):
    return hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"]
    ).decode("utf-8", "ignore")


def compare_passwords(hash, password):
    return hmac.compare_digest(
        base64.b64decode(hash),
        hashlib.pbkdf2_hmac(hash_name='sha256',
                            password=password.encode(),
                            salt=current_app.config["PWD_HASH_SALT"],
                            iterations=current_app.config["PWD_HASH_ITERATIONS"])
    )
