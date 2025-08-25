from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view

from content.models import Courses
from service.lectures import teacher_create_lecture
from content.models import Lecture
from .serializers import (
    StudentLectureSerializer,
    TeacherLectureSerializer,
    LectureCreateSerializer,
)
from api.permissions import IsTeacher
from content.models import StudentProfile

from schema.lectures.schemas import (
    teacher_lecture_create,
    teacher_lecture_delete,
    teacher_lecture_partial_update,
    teacher_lecture_retrieve,
    teacher_lecture_update,
    teacher_lectures_list,
    student_lectures_list,
)
from .filters import TeacherLectureFilter, LectureFilter


class BaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = TeacherLectureSerializer
    filterset_class = TeacherLectureFilter

    def get_queryset(self):
        teacher_profile = self.request.user.teacher_profile
        return Lecture.objects.for_teacher(teacher_profile)


# region teacher
@extend_schema_view(get=teacher_lectures_list, post=teacher_lecture_create)
class ListCreateLectureView(BaseAPIView, ListModelMixin, CreateModelMixin):
    """List and create lectures."""

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return LectureCreateSerializer
        return TeacherLectureSerializer

    def perform_create(self, serializer):
        teacher_profile = self.request.user.teacher_profile
        course_id = self.kwargs.get("course_id")
        lecture = teacher_create_lecture(teacher_profile, course_id, serializer.validated_data)
        serializer.instance = lecture


@extend_schema_view(
    get=teacher_lecture_retrieve,
    patch=teacher_lecture_partial_update,
    put=teacher_lecture_update,
    delete=teacher_lecture_delete,
)
class RetriveDestroyUpdateLectureView(BaseAPIView, RetrieveUpdateDestroyAPIView):
    """Manage specific lecture."""

    pass


# endregion
# region student
@extend_schema_view(get=student_lectures_list)
class ListStudentLectureView(ListAPIView):
    """List student lectures."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentLectureSerializer
    filterset_class = LectureFilter

    def get_queryset(self):
        student_profile = StudentProfile.objects.filter(user=self.request.user).first()
        if not student_profile:
            raise PermissionDenied("You are not a student.")
        return Lecture.objects.for_student(student_profile)


# endregion
