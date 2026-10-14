from datetime import datetime,timezone,timedelta
import hashlib
from pwdlib import PasswordHash
from app.core.config import settings
import jwt

password_hash = PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(user_id:int)->str:
    now=datetime.now(timezone.utc)

    payload={
        "sub":str(user_id),
        "type":"access",
        "iat":now,
        "exp":now+timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
