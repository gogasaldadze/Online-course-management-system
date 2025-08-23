from rest_framework import serializers


class TokenCreateSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
