from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)


from .serializers import (
    ListCoursesTeacherSerializer,
    ListCoursesStudentSerializer,
    CreateCoursesSerializer,
    UpdateCoursesSerializer,
    StudentRegisteredCoursesSerializer,
    AddHelperSerializer,
)

from content.models import Courses
from service.courses import create_course_with_students, update_course_students, manage_helpers

from api.permissions import IsMainTeacher, IsTeacher
from schema.serializers import (
    ValidationErrorSerializer,
    NotFoundSerializer,
    PermissionDeniedSerializer,
)
from schema.courses.schemas import (
    teacher_courses_list,
    teacher_course_create,
    teacher_course_delete,
    teacher_course_partial_update,
    teacher_course_retrieve,
    teacher_course_update,
    student_courses_available_list,
    student_courses_registered_list,
    student_course_registered_retrieve,
)

from .filters import CourseFilter, TeacherCourseFilter


# region teacher
@extend_schema_view(
    get=teacher_courses_list,
    post=teacher_course_create,
)
class TeacherCourseListCreateView(ListCreateAPIView):
    """List and create teacher courses."""

    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = "pk"
    filterset_class = TeacherCourseFilter

    def get_queryset(self):
        teacher_profile = getattr(self.request.user, "teacher_profile", None)
        return Courses.objects.for_teacher_optimized(teacher_profile)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateCoursesSerializer
        return ListCoursesTeacherSerializer

    def perform_create(self, serializer):
        teacher_profile = getattr(self.request.user, "teacher_profile")
        course = create_course_with_students(
            teacher=teacher_profile,
            name=serializer.validated_data.get("name"),
            available=serializer.validated_data.get("available", True),
            student_ids=serializer.validated_data.get("student_ids", []),
        )
        serializer.instance = course


@extend_schema_view(
    get=teacher_course_retrieve,
    put=teacher_course_update,
    patch=teacher_course_partial_update,
    delete=teacher_course_delete,
)
class TeacherCourseDetailView(RetrieveUpdateDestroyAPIView):
    """Manage specific teacher course."""

    permission_classes = [IsAuthenticated, IsMainTeacher]
    lookup_field = "pk"

    def get_queryset(self):
        teacher_profile = getattr(self.request.user, "teacher_profile")
        return Courses.objects.for_teacher_optimized(teacher_profile)

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return UpdateCoursesSerializer
        return ListCoursesTeacherSerializer

    def perform_update(self, serializer):
        students_add = serializer.validated_data.pop("student_add_ids", [])
        students_remove = serializer.validated_data.pop("student_remove_ids", [])
        instance = serializer.save()
        update_course_students(course=instance, add_ids=students_add, remove_ids=students_remove)


@extend_schema(
    tags=["Courses - Teacher"],
    operation_id="course_manage_helpers",
    summary="Manage helper teachers for course",
    description="Add or remove helper teachers from a course. Only the main teacher (owner) can manage helpers.",
    request=AddHelperSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)
class ManageHelpersView(UpdateAPIView):

    permission_classes = [IsAuthenticated, IsMainTeacher]
    serializer_class = AddHelperSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        return (
            Courses.objects.is_available()
            .with_teacher()
            .with_lectures()
            .with_helpers()
            .with_students()
            .only("id", "name", "teacher_id", "uuid")
        )

    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        helpers_add = serializer.validated_data.get("helpers_add_ids", [])
        helpers_remove = serializer.validated_data.get("helpers_remove_ids", [])
        manage_helpers(course=course, add_ids=helpers_add, remove_ids=helpers_remove)

        return Response(ListCoursesTeacherSerializer(course).data)


# endregion
# region student
@extend_schema_view(
    get=student_courses_available_list,
)
class StudentListCourseView(ListModelMixin, GenericAPIView):
    """List available courses."""

    serializer_class = ListCoursesStudentSerializer
    permission_classes = [AllowAny]
    filterset_class = CourseFilter

    def get_queryset(self):
        return Courses.objects.is_available().with_teacher().with_lectures().only_basic()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema_view(
    get=student_courses_registered_list,
)
class StudentRegisteredCoursesView(ListAPIView):
    """List student's registered courses."""

    serializer_class = StudentRegisteredCoursesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CourseFilter

    def get_queryset(self):
        student_profile = getattr(self.request.user, "student_profile", None)
        if not student_profile:
            raise PermissionDenied("You are not a student.")
        return Courses.objects.for_student_optimized(student_profile)


@extend_schema_view(
    get=student_course_registered_retrieve,
)
class StudentRegisteredCourseDetailView(RetrieveAPIView):
    """Get specific registered course."""

    serializer_class = StudentRegisteredCoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_profile = getattr(self.request.user, "student_profile", None)
        if not student_profile:
            raise PermissionDenied("You are not a student.")
        return Courses.objects.for_student_optimized(student_profile)


# endregion
