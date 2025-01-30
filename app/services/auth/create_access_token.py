import os
from datetime import datetime, timezone, timedelta

import jwt


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


def create_access_token(username: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
