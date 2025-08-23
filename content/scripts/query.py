from content.models import (
    Courses,
    Lecture,
    Homework,
    HomeWorkSubmission,
    StudentProfile,
    TeacherProfile,
    Grade,
    GradeComment,
)
from access.models import User
from django.db import connection

# python manage.py shell_plus --print-sql


def run():
    # student = User.objects.get(username="std1").student_profile
    # print(HomeWorkSubmission.objects.filter(student=student))
    pass
