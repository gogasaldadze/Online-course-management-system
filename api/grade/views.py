from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin

from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from content.models import Grade, HomeWorkSubmission, TeacherProfile
from .serializers import GradeSerializer
from api.permissions import IsHelper, IsMainTeacher
from .querysets import get_teachers_of_course


from schema.grades.schemas import (
    teacher_grades_list,
    teacher_grade_create,
    teacher_grade_update,
    student_grades_list,
)
from .filters import GradeFilter


# region teacher
@extend_schema_view(get=teacher_grades_list)
class GradeListView(GenericAPIView, ListModelMixin):
    """Endpoint for teachers to list grades for homework submissions."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    filterset_class = GradeFilter

    def get_queryset(self):
        teacher_profile = TeacherProfile.objects.filter(user=self.request.user).first()
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return get_teachers_of_course(teacher_profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema_view(post=teacher_grade_create)
class GradeCreateView(CreateAPIView):
    """Create a grade for a submission (only if it doesn't exist)."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return get_teachers_of_course(teacher_profile)

    def get_submission(self):
        submission_uuid = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return HomeWorkSubmission.objects.get(uuid=submission_uuid)
        except HomeWorkSubmission.DoesNotExist:
            raise NotFound("Submission not found.")

    def perform_create(self, serializer):
        submission = self.get_submission()
        self.check_object_permissions(self.request, submission)

        if Grade.objects.filter(submission=submission).exists():
            raise PermissionDenied("Grade already exists. Use update.")

        return serializer.save(submission=submission, graded=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grade = self.perform_create(serializer)
        return Response(self.get_serializer(grade).data, status=status.HTTP_201_CREATED)


@extend_schema_view(put=teacher_grade_update, patch=teacher_grade_update)
class GradeUpdateView(UpdateAPIView):
    """Update an existing grade (re-grade)."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return Grade.objects.filter(
            submission__in=get_teachers_of_course(teacher_profile)
        )

    def get_object(self):
        submission_uuid = self.kwargs.get(self.lookup_url_kwarg)
        try:
            submission = HomeWorkSubmission.objects.get(uuid=submission_uuid)
        except HomeWorkSubmission.DoesNotExist:
            raise NotFound("Submission not found.")

        try:
            return Grade.objects.get(submission=submission)
        except Grade.DoesNotExist:
            raise NotFound("Grade does not exist. Create it first.")

    def perform_update(self, serializer):
        grade = serializer.save(graded=True)
        submission = grade.submission
        submission.status = HomeWorkSubmission.Status.GRADED
        submission.save()


# endregion
# region student
@extend_schema_view(get=student_grades_list)
class StudentGradeListView(GenericAPIView, ListModelMixin):
    """Endpoint for students to view their own grades."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
        except AttributeError:
            raise PermissionDenied("Only students can view grades.")
        return Grade.objects.filter(submission__student=student_profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# endregion
