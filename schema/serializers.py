from rest_framework import serializers


class ErrorDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(required=False)


class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )


class PermissionDeniedSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(default="permission_denied")


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(default="not_found")
