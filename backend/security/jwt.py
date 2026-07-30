import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "TESTE"
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