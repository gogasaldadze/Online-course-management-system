from content.models import Courses, TeacherProfile, StudentProfile
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from service.courses import create_course_with_students, update_course_students


class TeacherSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ["id", "name"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["id", "name"]


class ListCoursesTeacherSerializer(serializers.ModelSerializer):
    student_quantity = serializers.IntegerField(read_only=True)
    teacher = TeacherSerilizer()
    student = StudentSerializer(many=True)
    helpers = TeacherSerilizer(many=True, read_only=True)

    class Meta:
        model = Courses
        fields = [
            "id",
            "uuid",
            "name",
            "teacher",
            "student",
            "helpers",
            "student_quantity",
        ]
        read_only_fields = ["id", "uuid"]


class ListCoursesStudentSerializer(serializers.ModelSerializer):
    teacher = TeacherSerilizer()
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = ["id", "name", "teacher", "lectures"]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_lectures(self, obj):

        if hasattr(obj, "prefetched_lectures"):
            return [{"id": l.id, "topic": l.topic} for l in obj.prefetched_lectures]
        return [{"id": l.id, "topic": l.topic} for l in obj.lectures.all()]


class CreateCoursesSerializer(serializers.ModelSerializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Courses
        fields = ["name", "available", "student_ids"]


class UpdateCoursesSerializer(serializers.ModelSerializer):
    student_add_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    student_remove_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Courses
        fields = ["name", "available", "student_add_ids", "student_remove_ids"]


class AddHelperSerializer(serializers.ModelSerializer):
    helpers_add_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    helpers_remove_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Courses
        fields = ["helpers_add_ids", "helpers_remove_ids"]


class StudentRegisteredCoursesSerializer(serializers.ModelSerializer):
    teacher = TeacherSerilizer()

    class Meta:
        model = Courses
        fields = [
            "id",
            "uuid",
            "name",
            "teacher",
            "created_at",
        ]
