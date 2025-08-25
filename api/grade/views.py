from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin

from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from content.models import Grade, HomeWorkSubmission, TeacherProfile
from service.grades import create_grade, update_grade
from .serializers import GradeSerializer
from api.permissions import IsHelper, IsMainTeacher
from content.models import Grade


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
    """List grades."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    filterset_class = GradeFilter

    def get_queryset(self):
        teacher_profile = TeacherProfile.objects.filter(user=self.request.user).first()
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return Grade.objects.for_teachers_of_course(teacher_profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema_view(post=teacher_grade_create)
class GradeCreateView(CreateAPIView):
    """Create grade."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return Grade.objects.for_teachers_of_course(teacher_profile)

    def get_submission(self):
        submission_uuid = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return HomeWorkSubmission.objects.get(uuid=submission_uuid)
        except HomeWorkSubmission.DoesNotExist:
            raise NotFound("Submission not found.")

    def perform_create(self, serializer):
        submission = self.get_submission()
        self.check_object_permissions(self.request, submission)
        grade = create_grade(submission.uuid, self.request.user.teacher_profile, serializer.validated_data)
        serializer.instance = grade

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grade = self.perform_create(serializer)
        return Response(self.get_serializer(grade).data, status=status.HTTP_201_CREATED)


@extend_schema_view(put=teacher_grade_update, patch=teacher_grade_update)
class GradeUpdateView(UpdateAPIView):
    """Update grade."""

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsMainTeacher | IsHelper]
    lookup_field = "uuid"
    lookup_url_kwarg = "submission_uuid"

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        if not teacher_profile:
            raise PermissionDenied("You are not a teacher!")
        return Grade.objects.for_teachers_of_course(teacher_profile)

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
        grade = update_grade(self.kwargs.get(self.lookup_url_kwarg), self.request.user.teacher_profile, serializer.validated_data)
        serializer.instance = grade


# endregion
# region student
@extend_schema_view(get=student_grades_list)
class StudentGradeListView(GenericAPIView, ListModelMixin):
    """List student grades."""

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
