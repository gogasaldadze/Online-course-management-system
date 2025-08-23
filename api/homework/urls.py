from django.urls import path, include
from .views import (
    RetrieveCreateHomeworkView,
    # UpdateDestroyHomeworkView,
    RetrieveHomeworkStudentView,
    StudentAllHomeworksView,
    ListHomeworkView,
)


urlpatterns = [
    # ------------------ Teacher Homework URLs ------------------
    # homework for a lecture or create a new one
    path(
        "teacher/<int:lecture_id>/",
        RetrieveCreateHomeworkView.as_view(),
        name="teacher-lecture-homeworks",
    ),
    path(
        "teacher/",
        ListHomeworkView.as_view(),
        name="get-all-homeworks-of-teacher",
    ),
    # ------------------Student Homework URLs -----------------
    path(
        "my/<int:lecture_id>/",
        RetrieveHomeworkStudentView.as_view(),
        name="student-specific-lecture-homeworks",
    ),
    path(
        "my/",
        StudentAllHomeworksView.as_view(),
        name="student-all-homeworks",
    ),
    path("", include("api.submission.urls")),
]
