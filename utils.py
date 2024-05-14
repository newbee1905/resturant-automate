from argon2 import PasswordHasher
import jwt
from datetime import datetime, timedelta, timezone

ph = PasswordHasher()

exp_time = timedelta(days=30)
# TODO: load from .env
secret = "secret"

def jwt_encode(payload):
	payload["exp"] = (datetime.now(tz=timezone.utc) + exp_time).timestamp()
	return jwt.encode(payload=payload, key=secret, algorithm="HS256")

def jwt_decode(token):
	return jwt.decode(token, key=secret, algorithms=["HS256"])
