from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.homework.serializers import (
    HomeworkCreateSerializer,
    HomeworkUpdateSerializer,
    StudentHomeworkSerializer,
)
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


student_homeworks_list = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_homeworks_list",
    summary="List lecture homework",
    description="Get homework for specific lecture",
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


student_homework_retrieve = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_homework_retrieve",
    summary="Get homework",
    description="Get homework assignment for student",
    responses={
        200: StudentHomeworkSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Homework not found",
        ),
    },
)


teacher_homeworks_list = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homeworks_list",
    summary="List lecture homework",
    description="Get homework for specific lecture",
    parameters=[
        OpenApiParameter(
            name="title",
            description="Homework title",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="status",
            description="Homework status",
            required=False,
            type=str,
            enum=["active", "inactive"],
        ),
    ],
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_homework_create = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_create",
    summary="Create homework",
    description="Create new homework assignment",
    request=HomeworkCreateSerializer,
    responses={
        201: StudentHomeworkSerializer,
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


teacher_homework_retrieve = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_retrieve",
    summary="Get homework",
    description="Get homework assignment details",
    responses={
        200: StudentHomeworkSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Homework not found",
        ),
    },
)


teacher_homework_update = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_update",
    summary="Update homework",
    description="Update homework assignment",
    request=HomeworkUpdateSerializer,
    responses={
        200: StudentHomeworkSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Homework not found",
        ),
    },
)


teacher_homework_partial_update = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_partial_update",
    summary="Update homework",
    description="Update homework assignment",
    request=HomeworkUpdateSerializer,
    responses={
        200: StudentHomeworkSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Homework not found",
        ),
    },
)


teacher_homework_delete = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_delete",
    summary="Delete homework",
    description="Delete homework assignment",
    responses={
        204: None,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Homework not found",
        ),
    },
)


student_all_homeworks_list = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_all_homeworks_list",
    summary="List all homeworks",
    description="Get all homework assignments for student",
    parameters=[
        OpenApiParameter(
            name="title",
            description="Homework title",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="status",
            description="Homework status",
            required=False,
            type=str,
            enum=["active", "inactive"],
        ),
        OpenApiParameter(
            name="course",
            description="Course ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_all_homeworks_list = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_all_homeworks_list",
    summary="List all homeworks",
    description="Get all homework assignments for teacher",
    parameters=[
        OpenApiParameter(
            name="title",
            description="Homework title",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="status",
            description="Homework status",
            required=False,
            type=str,
            enum=["active", "inactive"],
        ),
        OpenApiParameter(
            name="course",
            description="Course ID",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="lecture",
            description="Lecture ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)
