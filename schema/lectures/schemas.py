from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
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
    summary="List student lectures",
    description="Get lectures for enrolled courses",
    parameters=[
        OpenApiParameter(
            name="topic",
            description="Lecture topic",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="id",
            description="Lecture ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: StudentLectureSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_lectures_list = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lectures_list",
    summary="List teacher lectures",
    description="Get lectures for teacher's courses",
    parameters=[
        OpenApiParameter(
            name="topic",
            description="Lecture topic",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course_name",
            description="Course name",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: TeacherLectureSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_lecture_create = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_create",
    summary="Create lecture",
    description="Create new lecture",
    request=LectureCreateSerializer,
    responses={
        201: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Course not found",
        ),
    },
)


teacher_lecture_retrieve = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_retrieve",
    summary="Get lecture details",
    description="Get specific lecture details",
    responses={
        200: TeacherLectureSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Lecture not found",
        ),
    },
)


teacher_lecture_update = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_update",
    summary="Update lecture",
    description="Update lecture details",
    request=LectureCreateSerializer,
    responses={
        200: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Lecture not found",
        ),
    },
)


teacher_lecture_partial_update = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_partial_update",
    summary="Partial update lecture",
    description="Partially update lecture details",
    request=LectureCreateSerializer,
    responses={
        200: TeacherLectureSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Lecture not found",
        ),
    },
)


teacher_lecture_delete = extend_schema(
    tags=["Lectures - Teacher"],
    operation_id="teacher_lecture_delete",
    summary="Delete lecture",
    description="Delete lecture",
    responses={
        204: None,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Lecture not found",
        ),
    },
)
