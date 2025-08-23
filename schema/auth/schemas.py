# schema/auth/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from api.auth.serializers import RegisterSerializer
from api.auth.token.serializers import TokenCreateSerializer, TokenRefreshSerializer
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
    ErrorDetailSerializer,
)

# ==================== AUTHENTICATION SCHEMAS ====================
auth_register = extend_schema(
    tags=["Authentication"],
    operation_id="auth_register",
    summary="Register new user",
    request=RegisterSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="User registered successfully",
            examples=[
                OpenApiExample(
                    "Success", value={"message": "User registered successfully"}
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
    },
)

auth_logout = extend_schema(
    tags=["Authentication"],
    operation_id="auth_logout",
    summary="Logout user",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "example": "your_refresh_token_here"}
            },
        }
    },
    responses={
        status.HTTP_205_RESET_CONTENT: OpenApiResponse(
            description="Logged out successfully",
            examples=[
                OpenApiExample("Success", value={"message": "Logged out successfully"})
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ValidationErrorSerializer,
            description="Invalid token or validation error",
            examples=[
                OpenApiExample(
                    "Invalid Token Error", value={"error": "Invalid refresh token"}
                ),
                OpenApiExample(
                    "Validation Error", value={"refresh": ["This field is required."]}
                ),
            ],
        ),
    },
)

token_create = extend_schema(
    tags=["Authentication"],
    operation_id="token_create",
    summary="Obtain JWT token pair",
    description="Authenticate user credentials and return JWT access and refresh tokens.",
    request=TokenCreateSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Successfully authenticated and tokens generated",
            response={
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "JWT access token"},
                    "refresh": {"type": "string", "description": "JWT refresh token"},
                },
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ValidationErrorSerializer,
            description="Validation error - Invalid input data",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value={
                        "username": ["This field is required."],
                        "password": ["This field is required."],
                    },
                )
            ],
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=ErrorDetailSerializer,
            description="Authentication failed - Invalid credentials",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                        "detail": "No active account found with the given credentials",
                        "code": "no_active_account",
                    },
                )
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Login Request",
            value={"username": "johndoe", "password": "securepassword123"},
            request_only=True,
        )
    ],
)

token_refresh = extend_schema(
    tags=["Authentication"],
    operation_id="token_refresh",
    summary="Refresh JWT access token",
    description="Obtain a new access token using a valid refresh token.",
    request=TokenRefreshSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Successfully refreshed tokens",
            response={
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "New JWT access token"},
                    "refresh": {
                        "type": "string",
                        "description": "New JWT refresh token (if rotation enabled)",
                    },
                },
            },
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ValidationErrorSerializer,
            description="Validation error - Invalid or expired refresh token",
            examples=[
                OpenApiExample(
                    "Invalid Token",
                    value={
                        "detail": "Invalid Token",
                        "code": "invalid_token",
                    },
                ),
                OpenApiExample(
                    "Validation Error",
                    value={
                        "refresh": ["This field is required."],
                    },
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            "Refresh Request",
            value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
            request_only=True,
        )
    ],
)
