import os
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/login")

def authenticate(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    secret_key: str = os.environ["SECRET_KEY"]
    try:
        payload: Dict[str, Any] = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
