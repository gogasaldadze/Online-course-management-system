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
from .querysets import get_homework_submission, get_teachers_of_course
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
from rest_framework import filters
from .filters import SubmissionFilter
from django_filters.rest_framework import DjangoFilterBackend


# region teacher
@extend_schema_view(get=teacher_submissions_list, retrieve=teacher_submission_retrieve)
class SubmittedHomeworkView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    """Endpoint for teachers to view homework submissions for their courses."""

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
        return get_teachers_of_course(teacher_profile)

    def get(self, request, *args, **kwargs):
        if kwargs.get("uuid"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


# endregion
# region student


@extend_schema_view(post=student_submission_create)
class StudentHomeworkCreateView(CreateAPIView):
    """Endpoint for students to create homework submissions (POST /submit/<uuid:homework_uuid>/)."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        homework_uuid = self.kwargs.get("homework_uuid")
        if not homework_uuid:
            raise ValidationError({"homework": "Homework UUID is required."})

        try:
            homework = Homework.objects.get(uuid=homework_uuid)
        except Homework.DoesNotExist:
            raise ValidationError({"homework": "Invalid homework UUID"})

        student_profile = self.request.user.student_profile

        if HomeWorkSubmission.objects.filter(
            homework=homework, student=student_profile
        ).exists():
            raise ValidationError(
                {"homework": "You have already submitted this homework."}
            )

        instance = serializer.save(
            student=student_profile,
            status=HomeWorkSubmission.Status.SUBMITED,
            homework=homework,
        )


@extend_schema_view(put=student_submission_resubmit, patch=student_submission_resubmit)
class StudentHomeworkResubmitView(UpdateAPIView):
    """Endpoint for students to resubmit homework (PUT/PATCH /resubmit/<uuid:submission_uuid>/)."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return get_homework_submission(student_profile)

    def perform_update(self, serializer):
        submission_uuid = self.kwargs.get("submission_uuid")
        student_profile = getattr(self.request.user, "student_profile", None)

        try:
            existing_submission = HomeWorkSubmission.objects.get(
                student=student_profile, uuid=submission_uuid
            )
        except HomeWorkSubmission.DoesNotExist:
            raise ValidationError({"Submission": "Invalid homework submission UUID"})

        serializer.save(
            status=HomeWorkSubmission.Status.RESUBMITED,
            student=student_profile,
            homework=existing_submission.homework,
        )


@extend_schema_view(get=student_submissions_list)
class StudentHomeworkListView(ListAPIView):
    """Endpoint for students to list homework submissions."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    filterset_class = SubmissionFilter

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return get_homework_submission(student_profile)


@extend_schema_view(get=student_submission_retrieve)
class StudentHomeworkDetailView(RetrieveAPIView):
    """Endpoint for students to retrieve homework submissions."""

    serializer_class = HomeWorkSubmissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            raise PermissionDenied("You are not a student.")
        return get_homework_submission(student_profile)


# endregion
