from django.urls import path, include
from .views import (
    StudentHomeworkListView,
    SubmittedHomeworkView,
    StudentHomeworkDetailView,
    StudentHomeworkCreateView,
    StudentHomeworkResubmitView,
)

urlpatterns = [
    # =========== STUDENT ===========
    path(
        "submit/<uuid:homework_uuid>/",
        StudentHomeworkCreateView.as_view(),
        name="student-homework-submit",
    ),
    path("resubmit/<uuid:submission_uuid>/", StudentHomeworkResubmitView.as_view()),
    path(
        "submissions/",
        StudentHomeworkListView.as_view(),
        name="student-homework-submissions-list",
    ),
    path(
        "submissions/<uuid:uuid>/",
        StudentHomeworkDetailView.as_view(),
        name="student-homework-submission-detail",
    ),
    # ========== TEACHER =============
    path(
        "teacher/submitted/",
        SubmittedHomeworkView.as_view(),
        name="teacher-submitted-homeworks-list",
    ),
    path(
        "teacher/submitted/<uuid:uuid>/",
        SubmittedHomeworkView.as_view(),
        name="teacher-submitted-homeworks-detail",
    ),
    path("", include("api.grade.urls")),
    path("", include("api.comments.urls")),
]
