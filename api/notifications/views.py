from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema_view

from content.models import Notification
from .serializers import NotificationSerializer
from service.notifications import mark_read, mark_all_read
from schema.notifications.schemas import notifications_list, notification_mark_read


@extend_schema_view(get=notifications_list)
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


@extend_schema_view(patch=notification_mark_read)
class NotificationMarkReadView(UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    http_method_names = ["patch"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        mark_read(notification, True)
        return Response(NotificationSerializer(notification).data)


