import jwt
import hashlib
from datetime import datetime, timedelta, timezone

SECRET_KEY = "TESTETESTETESTETESTETESTETESTETESTETESTETESTETESTETESTE" #TOCHANGE
ALGORITHM = "HS256"

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def create_refresh_token(user_id: int,exp: datetime) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": exp
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def create_access_token(user_id: int) -> str:

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None