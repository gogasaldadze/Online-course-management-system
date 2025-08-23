from django.urls import path, include
from .views import (
    TeacherCourseListCreateView,
    TeacherCourseDetailView,
    StudentListCourseView,
    StudentRegisteredCoursesView,
    StudentRegisteredCourseDetailView,
    ManageHelpersView,
)


urlpatterns = [
    #  Student Course URLs
    path("", StudentListCourseView.as_view(), name="student-course-list"),
    path("my/", StudentRegisteredCoursesView.as_view(), name="student-my-courses"),
    path(
        "my/<int:pk>/",
        StudentRegisteredCourseDetailView.as_view(),
        name="student-my-course-detail",
    ),
    #  Teacher Course URLs
    path(
        "teacher/",
        TeacherCourseListCreateView.as_view(),
        name="teacher-course-list-create",
    ),
    path(
        "teacher/<int:pk>/",
        TeacherCourseDetailView.as_view(),
        name="teacher-course-detail",
    ),
    path(
        "teacher/<int:pk>/manage-helpers/",
        ManageHelpersView.as_view(),
        name="teacher-manage-helpers",
    ),
    #  Lectures urls
    path("", include("api.lectures.urls")),
]
