import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "TESTETESTETESTETESTETESTETESTETESTETESTETESTETESTETESTE"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=1)

    payload.update({
        "exp":expire
    })

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def decode_access_token(token: str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None