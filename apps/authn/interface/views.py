from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from apps.users.infrastructure.models import UserNode
from .serializers import LoginSerializer, RefreshSerializer, TokenPairOutSerializer, AccessOutSerializer
from ..tokens import make_jwt, decode_jwt
from common.api import ok  # success envelope
from common.exceptions import problem_response

from drf_spectacular.utils import extend_schema, OpenApiResponse
from common.schemas import Envelope, Problem

class LoginView(APIView):
    permission_classes = [AllowAny]   # public endpoint


    @extend_schema(
        tags=["Auth"],
        summary="Login (email + password) → JWT access/refresh",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(Envelope(TokenPairOutSerializer), description="Logged in."),
            400: Problem("validation_error"),
            401: Problem("invalid_credentials"),
        },
    )
    def post(self, request, *args, **kwargs):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower().strip()
        password = ser.validated_data["password"]

        user = UserNode.nodes.first_or_none(email=email, is_active=True)
        if not user or not check_password(password, user.password):
            # Neutral message on purpose (avoid account enumeration)
            return problem_response(
                request,
                status=status.HTTP_401_UNAUTHORIZED,
                title="Invalid credentials.",
                code="INVALID_CREDENTIALS",
                detail="The provided email or password is incorrect.",
                type_slug="unauthorized"
            )

        access = make_jwt(sub=user.uid, email=user.email, role=user.role, typ="access")
        refresh = make_jwt(sub=user.uid, email=user.email, role=user.role, typ="refresh")
        return ok(
            {
                "access": access,
                "refresh": refresh,
                "user": {
                    "id": user.uid,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "is_active": bool(user.is_active),
                },
            },
            code="LOGIN_SUCCESS",
            message="Logged in.",
            status=status.HTTP_200_OK,
            request=request,
        )

class RefreshView(APIView):
    permission_classes = [AllowAny]


    
    @extend_schema(
        tags=["Auth"],
        summary="Refresh access token",
        request=RefreshSerializer,  # contains 'refresh'
        responses={
            200: OpenApiResponse(Envelope(AccessOutSerializer), description="Access token refreshed."),
            400: Problem("validation_error"),
            401: Problem("invalid_token"),
        },
    )
    def post(self, request, *args, **kwargs):
        ser = RefreshSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data["refresh"]

        try:
            claims = decode_jwt(token)
        except Exception:
            return problem_response(
                request,
                status=status.HTTP_401_UNAUTHORIZED,
                title="Invalid or expired token.",
                code="INVALID_TOKEN",
                detail="The provided refresh token is invalid or expired.",
                type_slug="unauthorized"
            )

        if claims.get("typ") != "refresh":
            return problem_response(
                request,
                status=status.HTTP_401_UNAUTHORIZED,
                title="Wrong token type.",
                code="WRONG_TOKEN_TYPE",
                detail="The provided token is not a refresh token.",
                type_slug="unauthorized"
            )

        # (Optional) look up user to ensure still active (revocation check).
        user = UserNode.nodes.get_or_none(uid=claims["sub"])
        if not user or not user.is_active:
            
            return problem_response(
                request,
                status=status.HTTP_401_UNAUTHORIZED,
                title="User inactive.",
                code="USER_INACTIVE",
                detail="The user is inactive or does not exist.",
                type_slug="unauthorized"
            )

        new_access = make_jwt(sub=claims["sub"], email=claims.get("email",""), role=claims.get("role",""), typ="access")
        new_refresh = make_jwt(sub=claims["sub"], email=claims.get("email",""), role=claims.get("role",""), typ="refresh")

        return ok(
            {"access": new_access, "refresh": new_refresh},
            code="TOKEN_REFRESHED",
            message="Tokens refreshed.",
            request=request,
        )
