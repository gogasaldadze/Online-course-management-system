# schema/notifications/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.notifications.serializers import NotificationSerializer
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


notifications_list = extend_schema(
    tags=["Notifications"],
    operation_id="notifications_list",
    summary="List user notifications",
    description="Get user notifications",
    responses={
        200: NotificationSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


notification_mark_read = extend_schema(
    tags=["Notifications"],
    operation_id="notification_mark_read",
    summary="Mark notification as read",
    description="Mark notification as read",
    responses={
        200: NotificationSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Notification not found",
        ),
    },
)
