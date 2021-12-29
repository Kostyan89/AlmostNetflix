import base64

import hashlib
import hmac

from flask import current_app


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def get_hash(password):
    return generate_password_digest(password).decode("utf-8", "ignore")


def compare_passwords(hash, password):
    return hmac.compare_digest(
        base64.b64decode(hash), generate_password_digest(password)
    )
