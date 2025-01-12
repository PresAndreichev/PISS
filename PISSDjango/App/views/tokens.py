import jwt
from datetime import datetime, timedelta


SECRET_KEY = "ROSITSA_SILVIA_ANTOAN_PRESIAN"
TOKEN_EXPIRATION_HOURS = 24

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(hours=TOKEN_EXPIRATION_HOURS),  # Expiration time
        "iat": datetime.now()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
