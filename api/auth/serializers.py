from rest_framework import serializers
from access.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Roles.choices)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "role", "name"]

    def create(self, validated_data):
        name = validated_data.pop("name")
        password = validated_data.pop("password")
        role = validated_data.pop("role")

        user = User.objects.create_user(
            username=validated_data.pop("username"),
            password=password,
            role=role,
            name=name,
        )

        return user
