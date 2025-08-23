from django.urls import path
from .views import GradeListView, StudentGradeListView, GradeCreateView, GradeUpdateView

urlpatterns = [
    # Teacher
    path("teacher/grades/", GradeListView.as_view(), name="grade-list"),
    path(
        "teacher/grades/create/<uuid:submission_uuid>/",
        GradeCreateView.as_view(),
        name="grade-create",
    ),
    path(
        "teacher/grades/update/<uuid:submission_uuid>/",
        GradeUpdateView.as_view(),
        name="grade-update",
    ),
    # Student
    path("my/grades/", StudentGradeListView.as_view(), name="student-grade-list"),
]
