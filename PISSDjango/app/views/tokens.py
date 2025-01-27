import jwt
from datetime import datetime, timedelta

SECRET_KEY = "ROSITSA_SILVIA_ANTOAN_PRESIAN"
TOKEN_EXPIRATION_HOURS = 24

def generate_token(user_id):
    try:
        curr_time = datetime.utcnow()
        exp_time = curr_time + timedelta(hours=TOKEN_EXPIRATION_HOURS)
        
        payload = {
            "user_id": user_id,
            "exp": int(exp_time.timestamp()),  # Expiration time
            "iat": int(curr_time.timestamp())  # Issued at
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Token generation failed: {str(e)}")
    
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
