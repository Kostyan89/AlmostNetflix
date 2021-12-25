import base64
import hashlib
import hmac

from flask import current_app

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
        'sha256',
        password.encode('utf-8'),
        BaseConfig.PWD_HASH_SALT,
        BaseConfig.PWD_HASH_ITERATIONS
    ).decode("utf-8", "ignore")


def compare_passwords(get_hash, password):
    return hmac.compare_digest(
        base64.b64decode(get_hash),
        hashlib.pbkdf2_hmac('sha256', password.encode(), BaseConfig.PWD_HASH_SALT, BaseConfig.PWD_HASH_ITERATIONS))
