import os
import secrets
import string
from base64 import b64encode
from hashlib import pbkdf2_hmac


_ACCESS_KEY_LETTERS = string.ascii_uppercase + string.digits
_SECRET_LETTERS = string.ascii_letters + string.digits + '+/-_'


def generate_id(prefix='CKIC', length=20):
    # AKDC stands for Access Key Dalibo Cornac.
    return prefix + ''.join(secrets.choice(_ACCESS_KEY_LETTERS)
                            for _ in range(length - len(prefix)))


def generate_secret(length=40):
    return ''.join(secrets.choice(_SECRET_LETTERS) for _ in range(length))


def generate_session_token(length=258):
    return b64encode(os.urandom(length)).decode('ascii')


def hash_password(password, salt):
    return b64encode(pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        1_000_000,
    )).decode('ascii')
