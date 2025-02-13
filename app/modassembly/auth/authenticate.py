import os
from typing import Any, Dict

import jwt


def authenticate(token: str) -> Dict[str, Any]:
    secret_key: str = os.environ["SECRET_KEY"]
    algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
    payload: Dict[str, Any] = jwt.decode(token, secret_key, algorithms=[algorithm])
    return payload
