import os
from typing import Final
import bcrypt

# Retrieve the bcrypt salt rounds from environment variables, default to 12 if not set.
BCRYPT_ROUNDS: Final[int] = int(os.environ.get("BCRYPT_ROUNDS", 12))

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt with the number of rounds defined by the environment variable BCRYPT_ROUNDS.
    Returns the hashed password as a UTF-8 string.
    """
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")
