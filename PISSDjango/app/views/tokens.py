import jwt
from datetime import datetime, timedelta

SECRET_KEY = "ROSITSA_SILVIA_ANTOAN_PRESIAN"
TOKEN_EXPIRATION_HOURS = 24

def generate_token(user_id, username, role):
    """Generates JWT token with the given credentials inside"""
    try:
        curr_time = datetime.utcnow()
        exp_time = curr_time + timedelta(hours=TOKEN_EXPIRATION_HOURS)
        
        payload = {
            "user_id": user_id,
            "username" : username,            
            "role": role,
            "exp": int(exp_time.timestamp()),  # Expiration time
            "iat": int(curr_time.timestamp()),  # Issued at
        }
        
        encoded_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        print("no exception after encoding token")
        return encoded_token
    except Exception as e:
        raise RuntimeError(f"Token generation failed: {str(e)}")
    
def decode_token(token):
    """Parses the credentials (user_id, username and role) from a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "user_id": payload.get("user_id"),
            "username": payload.get("username"),
            "role": payload.get("role"),
        }
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
