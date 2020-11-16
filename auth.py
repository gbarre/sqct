from hashlib import sha256
from models import User


def basic_auth(username, password, required_scopes=None):
    user = User.query.get(username)
    if user is not None and user.password is not None:
        if sha256(password.encode('utf-8')).hexdigest() == user.password:
            return {'sub': user.id, 'scope': 'basic'}

    return None


def admin_auth(username, password, required_scopes=None):
    user = User.query.get(username)
    if user is not None and user.password is not None and user.id == "gbarre2":
        if sha256(password.encode('utf-8')).hexdigest() == user.password:
            return {'sub': user.id, 'scope': 'admin'}

    return None
