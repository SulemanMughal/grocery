from typing import Tuple, Optional
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .tokens import decode_jwt

class Principal:
    """
    Lightweight "user" object (no django.contrib.auth dependency).
    """
    def __init__(self, user_id: str, email: str, role: str):
        self.id = user_id
        self.email = email
        self.role = role
        self.is_authenticated = True

    # DRF sometimes checks these
    @property
    def pk(self): return self.id
    def __str__(self): return f"Principal<{self.email}:{self.role}>"

class CustomJWTAuthentication(BaseAuthentication):
    """
    Reads Authorization: Bearer <access_token>, validates with PyJWT,
    and returns a Principal + claims dict.
    """
    www_authenticate_realm = "api"

    def authenticate(self, request) -> Optional[Tuple[Principal, dict]]:
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"bearer":
            return None  # let other authenticators run or ultimately be anonymous
        if len(auth) == 1:
            raise AuthenticationFailed("Invalid Authorization header. No credentials provided.")
        if len(auth) > 2:
            raise AuthenticationFailed("Invalid Authorization header. Token string should not contain spaces.")

        token = auth[1].decode("utf-8")
        try:
            claims = decode_jwt(token)
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token.") from e

        if claims.get("typ") != "access":
            raise AuthenticationFailed("Wrong token type.")

        principal = Principal(
            user_id=claims["sub"],
            email=claims.get("email", ""),
            role=claims.get("role", ""),
        )
        # optionally expose claims to views/permissions
        request.jwt_claims = claims
        return principal, claims

    def authenticate_header(self, request):
        return 'Bearer realm="%s"' % self.www_authenticate_realm
