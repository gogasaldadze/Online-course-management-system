from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from api.homework.serializers import (
    HomeworkCreateSerializer,
    HomeworkUpdateSerializer,
    StudentHomeworkSerializer,
)
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


student_homeworks_list = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_homeworks_list",
    summary="List student's homework",
    description="Retrieve all homework assignments for courses where the student is enrolled.",
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

student_homework_retrieve = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_homework_retrieve",
    summary="Retrieve student's homework",
    description="Retrieve detailed information about a specific homework assignment for the student.",
    responses={
        200: StudentHomeworkSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)


teacher_homeworks_list = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homeworks_list",
    summary="List teacher's homework",
    description="Retrieve all homework assignments created by the authenticated teacher.",
    responses={
        200: HomeworkCreateSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

teacher_homework_create = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_create",
    summary="Create a new homework",
    description="Create a new homework assignment for a lecture.",
    request=HomeworkCreateSerializer,
    responses={
        201: HomeworkCreateSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_homework_retrieve = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_retrieve",
    summary="Retrieve teacher's homework",
    description="Retrieve details of a specific homework assignment created by the teacher.",
    responses={
        200: HomeworkCreateSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_homework_update = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_update",
    summary="Update a homework",
    description="Full update of a homework assignment.",
    request=HomeworkUpdateSerializer,
    responses={
        200: HomeworkCreateSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_homework_partial_update = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_partial_update",
    summary="Partially update a homework",
    description="Partial update of a homework assignment.",
    request=HomeworkUpdateSerializer,
    responses={
        200: HomeworkCreateSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_homework_delete = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_homework_delete",
    summary="Delete a homework",
    description="Delete a homework assignment created by the teacher.",
    responses={
        204: OpenApiResponse(description="Homework deleted successfully"),
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)


student_all_homeworks_list = extend_schema(
    tags=["Homework - Student"],
    operation_id="student_all_homeworks_list",
    summary="List all student's homework across all courses",
    description="Retrieve all homework assignments across all courses the student is enrolled in.",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by homework status",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course", description="Filter by course ID", required=False, type=int
        ),
    ],
    responses={
        200: StudentHomeworkSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

teacher_all_homeworks_list = extend_schema(
    tags=["Homework - Teacher"],
    operation_id="teacher_all_homeworks_list",
    summary="List all teacher's homework across all courses",
    description="Retrieve all homework assignments across all courses taught by the teacher.",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by homework status",
            required=False,
            type=str,
            enum=[
                "draft",
                "published",
                "archived",
            ],
        ),
        OpenApiParameter(
            name="course_id",
            description="Filter by course ID",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="lecture_id",
            description="Filter by lecture ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: HomeworkCreateSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)
