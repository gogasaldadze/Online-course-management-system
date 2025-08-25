from rest_framework import serializers
from content.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "uuid", "title", "message", "is_read", "created_at"]
        read_only_fields = ["id", "uuid", "created_at"]



