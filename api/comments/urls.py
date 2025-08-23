from django.urls import path
from .views import GradeCommentListCreateView

urlpatterns = [
    path(
        "<uuid:grade_uuid>/comments/",
        GradeCommentListCreateView.as_view(),
        name="grade-comments",
    ),
]
