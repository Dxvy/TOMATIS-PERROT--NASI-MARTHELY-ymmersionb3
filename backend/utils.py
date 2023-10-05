import base64
import hashlib
from werkzeug.security import check_password_hash


def convert_to_base64(image):
    return base64.b64encode(image).decode('utf-8')


def generate_salt():
    return hashlib.sha512().hexdigest()[:16]
