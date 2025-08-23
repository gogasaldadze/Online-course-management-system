from django.urls import path
from .views import (
    ListCreateLectureView,
    RetriveDestroyUpdateLectureView,
    ListStudentLectureView,
)


urlpatterns = [
    # Student Lectures URLs
    path(
        "my/<int:pk>/lectures/",
        ListStudentLectureView.as_view(),
        name="student-my-course-lectures",
    ),
    # Teacher Lectures Urls
    path(
        "teacher/<int:course_id>/lectures/",
        ListCreateLectureView.as_view(),
        name="teacher-course-lectures",
    ),
    path(
        "teacher/lectures/<int:pk>/",
        RetriveDestroyUpdateLectureView.as_view(),
        name="teacher-lecture-detail",
    ),
]
