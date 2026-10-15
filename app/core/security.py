from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return cast(str, pwd_context.hash(password))


def verify_password(plain: str, hashed: str) -> bool:
    return cast(bool, pwd_context.verify(plain, hashed))


def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload: dict[str, Any] = {"sub": str(subject), "exp": expire}
    return cast(str, jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM))


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        return cast(
            dict[str, Any], jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        )
    except JWTError:
        return None
