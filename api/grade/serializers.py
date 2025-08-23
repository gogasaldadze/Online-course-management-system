from rest_framework import serializers
from content.models import Grade
from api.courses.serializers import StudentSerializer


class GradeSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(read_only=True)
    student = StudentSerializer(source="submission.student", read_only=True)

    class Meta:
        model = Grade
        fields = ["student", "id", "uuid", "submission", "points", "graded", "feedback"]
        read_only_fields = ["id", "uuid", "graded", "student"]
