from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema_view

from content.models import Homework
from .serializers import (
    HomeworkCreateSerializer,
    HomeworkUpdateSerializer,
    StudentHomeworkSerializer,
)
from api.permissions import IsTeacher
from content.models import Lecture
from service.homework import teacher_create_homework
from content.models import StudentProfile

from schema.homework.schemas import (
    teacher_homeworks_list,
    teacher_homework_create,
    teacher_homework_partial_update,
    teacher_homework_delete,
    student_homework_retrieve,
    student_all_homeworks_list,
    teacher_all_homeworks_list,
)
from .filters import HomeworkFilter


# region teacher
class BaseAPIView(GenericAPIView):
    serializer_class = HomeworkCreateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        lecture_id = self.kwargs.get("lecture_id")
        return Homework.objects.for_teacher(teacher_profile, lecture_id)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return HomeworkUpdateSerializer
        return HomeworkCreateSerializer


@extend_schema_view(
    get=teacher_homeworks_list,
    post=teacher_homework_create,
    patch=teacher_homework_partial_update,
    delete=teacher_homework_delete,
)
class RetrieveCreateHomeworkView(
    BaseAPIView, ListModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
):
    """Manage homework for lecture."""

    lookup_field = "lecture_id"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile
        lecture_id = self.kwargs.get("lecture_id")
        hw = teacher_create_homework(teacher_profile, lecture_id, serializer.validated_data)
        serializer.instance = hw


@extend_schema_view(get=teacher_all_homeworks_list)
class ListHomeworkView(BaseAPIView, ListModelMixin):

    filterset_class = HomeworkFilter

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        return Homework.objects.for_teacher_all(teacher_profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# endregion
# region student
@extend_schema_view(get=student_homework_retrieve)
class RetrieveHomeworkStudentView(RetrieveAPIView):
    """Get homework for student."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentHomeworkSerializer
    lookup_field = "lecture_id"

    def get_object(self):
        student_profile = StudentProfile.objects.filter(user=self.request.user).first()
        if not student_profile:
            raise PermissionDenied("You are not a student.")

        lecture_id = self.kwargs.get("lecture_id")

        return get_object_or_404(
            Homework, lecture_id=lecture_id, lecture__course__student=student_profile
        )


@extend_schema_view(get=student_all_homeworks_list)
class StudentAllHomeworksView(ListAPIView):
    """List all student homeworks."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentHomeworkSerializer
    filterset_class = HomeworkFilter

    def get_queryset(self):
        student_profile = StudentProfile.objects.filter(user=self.request.user).first()
        if not student_profile:
            raise PermissionDenied("You are not a student.")
        return Homework.objects.for_student(student_profile)


# endregion
