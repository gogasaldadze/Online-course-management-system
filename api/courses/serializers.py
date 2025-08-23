from content.models import Courses, TeacherProfile, StudentProfile
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


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
    )  # replaced PrimaryKeyRelatedField because it was cousing 40 + queries

    class Meta:
        model = Courses
        fields = ["name", "available", "student_ids"]

    def validate_student_ids(self, value):
        existing_students = StudentProfile.objects.filter(id__in=value)

        existing_ids = [student.id for student in existing_students]

        missing = [i for i in value if i not in existing_ids]

        if missing:
            raise serializers.ValidationError(f"Invalid student IDs: {missing}")

        return value

    def create(self, validated_data):
        student_ids = validated_data.pop("student_ids")
        course = Courses.objects.create(**validated_data)
        course.student.add(*student_ids)
        return course


class UpdateCoursesSerializer(serializers.ModelSerializer):

    student_add_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    student_remove_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Courses
        fields = [
            "name",
            "available",
            "student_add_ids",
            "student_remove_ids",
        ]

    def validate_student_ids(self, value):
        existing_ids = [
            student.id for student in StudentProfile.objects.filter(id__in=value)
        ]

        missing_ids = [id for id in value if id not in existing_ids]

        if missing_ids:
            raise serializers.ValidationError(f"Invalid student IDs{missing_ids}")

        return value

    def validate_student_add_ids(self, value):
        return self.validate_student_ids(value)

    def validate_student_remove_ids(self, value):
        return self.validate_student_ids(value)

    def update(self, instance, validated_data):
        students_add = validated_data.pop("student_add_ids", [])
        students_remove = validated_data.pop("student_remove_ids", [])

        instance = super().update(instance, validated_data)

        if students_add:
            students = StudentProfile.objects.filter(id__in=students_add)
            instance.student.add(*students)

        if students_remove:
            students = StudentProfile.objects.filter(id__in=students_remove)
            instance.student.remove(*students)

        return instance


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

    def validate_helpers_ids(self, value):
        existing_ids = list(
            TeacherProfile.objects.filter(id__in=value).values_list("id", flat=True)
        )

        missing_ids = [id_ for id_ in value if id_ not in existing_ids]

        if missing_ids:
            raise serializers.ValidationError(f"Invalid helper IDs: {missing_ids}")

        return value

    def validate_helpers_add_ids(self, value):
        return self.validate_helpers_ids(value)

    def validate_helpers_remove_ids(self, value):
        return self.validate_helpers_ids(value)


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
