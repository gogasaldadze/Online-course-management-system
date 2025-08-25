from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsTeacher
from .serializers import HomeWorkSubmissionSerializer, SubmittedHomeworkSerializer
from content.models import HomeWorkSubmission
from drf_spectacular.utils import extend_schema_view

from schema.submission.schemas import (
    student_submissions_list,
    student_submission_create,
    teacher_submissions_list,
    student_submission_resubmit,
    student_submission_retrieve,
    teacher_submission_retrieve,
)

from rest_framework.exceptions import ValidationError, PermissionDenied

from content.models import Homework, StudentProfile, HomeWorkSubmission
from service.submissions import create_submission, resubmit_submission
from rest_framework import filters
from .filters import SubmissionFilter
from django_filters.rest_framework import DjangoFilterBackend


# region teacher
@extend_schema_view(get=teacher_submissions_list, retrieve=teacher_submission_retrieve)
class SubmittedHomeworkView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    """View homework submissions."""

    serializer_class = SubmittedHomeworkSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = "uuid"
    filterset_class = SubmissionFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["homework__title", "status"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        return HomeWorkSubmission.objects.for_teachers_of_course(teacher_profile)

    def get(self, request, *args, **kwargs):
        if kwargs.get("uuid"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


# endregion
# region student


@extend_schema_view(post=student_submission_create)
class StudentHomeworkCreateView(CreateAPIView):
    """Submit homework."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        homework_uuid = self.kwargs.get("homework_uuid")
        student_profile = self.request.user.student_profile
        instance = create_submission(homework_uuid, student_profile, serializer.validated_data)
        serializer.instance = instance


@extend_schema_view(put=student_submission_resubmit, patch=student_submission_resubmit)
class StudentHomeworkResubmitView(UpdateAPIView):
    """Resubmit homework."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return HomeWorkSubmission.objects.for_student(student_profile)

    def perform_update(self, serializer):
        submission_uuid = self.kwargs.get("submission_uuid")
        student_profile = getattr(self.request.user, "student_profile", None)
        instance = resubmit_submission(submission_uuid, student_profile, serializer.validated_data)
        serializer.instance = instance


@extend_schema_view(get=student_submissions_list)
class StudentHomeworkListView(ListAPIView):
    """List student submissions."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    filterset_class = SubmissionFilter

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return HomeWorkSubmission.objects.for_student(student_profile)


@extend_schema_view(get=student_submission_retrieve)
class StudentHomeworkDetailView(RetrieveAPIView):
    """Get submission details."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return HomeWorkSubmission.objects.for_student(student_profile)


# endregion
