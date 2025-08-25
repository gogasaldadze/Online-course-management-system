from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.grade.serializers import GradeSerializer
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


teacher_grades_list = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grades_list",
    summary="List grades",
    description="Get grades for teacher's courses",
    parameters=[
        OpenApiParameter(
            name="score",
            description="Grade score",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="feedback",
            description="Grade feedback",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="submission",
            description="Submission UUID",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: GradeSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_grade_create = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grade_create",
    summary="Create grade",
    description="Create new grade for submission",
    request=GradeSerializer,
    responses={
        201: GradeSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Submission not found",
        ),
    },
)


teacher_grade_update = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grade_update",
    summary="Update grade",
    description="Update existing grade",
    request=GradeSerializer,
    responses={
        200: GradeSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer,
            description="Grade not found",
        ),
    },
)


student_grades_list = extend_schema(
    tags=["Grades - Student"],
    operation_id="student_grades_list",
    summary="List student grades",
    description="Get grades for student's submissions",
    parameters=[
        OpenApiParameter(
            name="score",
            description="Grade score",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="feedback",
            description="Grade feedback",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: GradeSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)
