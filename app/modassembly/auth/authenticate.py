import os
from typing import Any, Dict

import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize HTTPBearer instance for dependency injection if needed
security = HTTPBearer()

def authenticate(token: str) -> Dict[str, Any]:
    """
    Verifies the JWT token using the secret key from environment variables.
    Returns the decoded token payload on success.

    Parameters:
        token (str): The JWT token as a string.

    Returns:
        Dict[str, Any]: The decoded payload of the JWT token.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded.
    """
    secret_key: str = os.environ["SECRET_KEY"]

    # Decode the JWT token using the HS256 algorithm.
    # Let any jwt exceptions propagate as HTTP errors.
    try:
        payload: Dict[str, Any] = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token"
        ) from exc

    return payload
