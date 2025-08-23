from rest_framework import serializers
from content.models import GradeComment
from drf_spectacular.utils import extend_schema_field


class GradeCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_type = serializers.SerializerMethodField()

    class Meta:
        model = GradeComment
        fields = ["id", "author_name", "author_type", "text", "created_at"]
        read_only_fields = ["author_name", "author_type", "created_at"]

    @extend_schema_field(serializers.CharField())
    def get_author_name(self, obj):
        user = obj.author
        if hasattr(user, "teacher_profile"):
            return user.teacher_profile.name
        elif hasattr(user, "student_profile"):
            return user.student_profile.name
        return user.username

    @extend_schema_field(serializers.CharField())
    def get_author_type(self, obj):
        user = obj.author
        if hasattr(user, "teacher_profile"):
            return "teacher"
        elif hasattr(user, "student_profile"):
            return "student"
        return "user"
