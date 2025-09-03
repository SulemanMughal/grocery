import uuid, time, jwt
from datetime import datetime, timezone
from .config import (
    JWT_SECRET, JWT_ALGORITHM, JWT_ISSUER, JWT_AUDIENCE,
    JWT_ACCESS_LIFETIME, JWT_REFRESH_LIFETIME
)

def _now():
    return datetime.now(timezone.utc)

def _ts(dt):
    return int(dt.timestamp())

def make_jwt(*, sub: str, email: str, role: str, typ: str):
    """
    typ: "access" or "refresh"
    """
    assert typ in {"access", "refresh"}
    now = _now()
    exp = now + (JWT_ACCESS_LIFETIME if typ == "access" else JWT_REFRESH_LIFETIME)
    payload = {
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": _ts(now),
        "nbf": _ts(now),
        "exp": _ts(exp),
        "jti": uuid.uuid4().hex,
        "sub": sub,          # user id
        "email": email,
        "role": role,
        "typ": typ,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token: str):
    """
    Raises jwt.InvalidTokenError / jwt.ExpiredSignatureError on failure.
    """
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        audience=JWT_AUDIENCE,
        issuer=JWT_ISSUER,
        options={"require": ["exp", "iat", "nbf", "iss", "aud", "sub", "typ"]},
    )
