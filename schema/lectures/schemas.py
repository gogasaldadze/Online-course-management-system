from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.lectures.serializers import (
    StudentLectureSerializer,
    TeacherLectureSerializer,
    LectureCreateSerializer,
)
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


student_lectures_list = extend_schema(
    tags=["Lectures - Student"],
    operation_id="student_lectures_list",
    summary="List student's lectures",
    description="Retrieve all lectures for courses where the student is enrolled.",
    responses={
        200: StudentLectureSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)


teacher_lectures_list = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lectures_list",
    summary="List teacher's lectures",
    description="Retrieve all lectures for courses where the user is a teacher.",
    responses={
        200: TeacherLectureSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

teacher_lecture_create = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_create",
    summary="Create a new lecture",
    description="Create a new lecture for a course where the user is a teacher.",
    request=LectureCreateSerializer,
    responses={
        201: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_lecture_retrieve = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_retrieve",
    summary="Retrieve teacher's lecture",
    description="Retrieve details of a specific lecture where the user is a teacher.",
    responses={
        200: TeacherLectureSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_lecture_update = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_update",
    summary="Update a lecture",
    description="Full update of a lecture where the user is a teacher.",
    request=LectureCreateSerializer,
    responses={
        200: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_lecture_partial_update = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_partial_update",
    summary="Partially update a lecture",
    description="Partial update of a lecture where the user is a teacher.",
    request=LectureCreateSerializer,
    responses={
        200: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_lecture_delete = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_delete",
    summary="Delete a lecture",
    description="Delete a lecture where the user is a teacher.",
    responses={
        204: OpenApiResponse(description="Lecture deleted successfully"),
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)
