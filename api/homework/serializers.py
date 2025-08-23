from rest_framework import serializers

from content.models import Homework, Lecture


class HomeworkCreateSerializer(serializers.ModelSerializer):
    lecture_name = serializers.CharField(source="lecture.topic", read_only=True)

    class Meta:
        model = Homework
        fields = [
            "id",
            "uuid",
            "created_at",
            "updated_at",
            "lecture",
            "lecture_name",
            "title",
            "description",
        ]

        read_only_fields = ["id", "uuid", "created_at", "updated_at", "lecture"]


class HomeworkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ["title", "description"]


class StudentHomeworkSerializer(serializers.ModelSerializer):

    lecture_name = serializers.CharField(source="lecture.topic", read_only=True)

    class Meta:
        model = Homework
        fields = ["id", "uuid", "title", "description", "lecture_name"]
