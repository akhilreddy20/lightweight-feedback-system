from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from config import ALGORITHM, SECRET_KEY, TOKEN_TTL_MINUTES

# bcrypt is used directly: passlib is unmaintained and crashes with bcrypt>=4.1
# ("password cannot be longer than 72 bytes" during its self-test).
# Hashes are standard $2b$ strings, so accounts created earlier still verify.


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
