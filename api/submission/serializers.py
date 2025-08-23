from rest_framework import serializers
from content.models import HomeWorkSubmission


class HomeWorkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWorkSubmission
        fields = [
            "id",
            "uuid",
            "student",
            "homework",
            "text_submission",
            "submitted_file",
            "status",
        ]
        read_only_fields = ["id", "student", "homework", "status", "uuid"]


class SubmittedHomeworkSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(source="student.name", read_only=True)
    homework_name = serializers.CharField(source="homework.title", read_only=True)

    class Meta:
        model = HomeWorkSubmission
        fields = [
            "id",
            "uuid",
            "created_at",
            "updated_at",
            "student",
            "student_name",
            "homework",
            "homework_name",
            "text_submission",
            "submitted_file",
            "status",
        ]

        read_only_fields = ["id", "uuid", "created_at", "updated_at"]
