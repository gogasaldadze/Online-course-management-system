from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from api.exceptions import BadRequest
from .serializers import TokenCreateSerializer, TokenRefreshSerializer
from api.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view
from schema.auth.schemas import token_create, token_refresh


@extend_schema_view(post=token_create)
class TokenCreateView(jwt_views.TokenViewBase):
    serializer_class = TokenCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password"),
        )

        if not user:
            raise AuthenticationFailed(
                {
                    "detail": "No active account found with the given credentials",
                    "code": "no_active_account",
                }
            )

        try:
            refresh = RefreshToken.for_user(user)

        except TokenError:
            raise BadRequest({"detail": "Invalid Token", "code": "invalid_token"})

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status.HTTP_200_OK,
        )


@extend_schema_view(post=token_refresh)
class TokenRefreshView(jwt_views.TokenViewBase):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh = RefreshToken(serializer.validated_data.get("refresh"))

        except TokenError:
            raise BadRequest({"detail": "Invalid Token", "code": "invalid_token"})

        if jwt_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status.HTTP_200_OK,
        )
