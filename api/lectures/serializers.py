from content.models import Lecture
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class StudentLectureSerializer(serializers.ModelSerializer):
    presentation_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Lecture
        fields = ["id", "topic", "presentation_file"]

        read_only_fields = ["id"]


class TeacherLectureSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(source="course.name", read_only=True)
    teacher_names = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            "id",
            "uuid",
            "created_at",
            "updated_at",
            "course",
            "course_name",
            "topic",
            "presentation_file",
            "teacher_names",
        ]

        read_only_fields = [
            "id",
            "uuid",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_teacher_names(self, obj):
        return [obj.course.teacher.name]


class LectureCreateSerializer(serializers.ModelSerializer):

    presentation_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Lecture
        fields = ["topic", "presentation_file"]
