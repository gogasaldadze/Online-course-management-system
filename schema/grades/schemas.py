from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.grade.serializers import GradeSerializer
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


teacher_grades_list = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grades_list",
    summary="List grades for teacher's courses",
    description="Retrieve all grades for homework submissions in courses where the user is a teacher or helper.",
    responses={
        200: GradeSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

teacher_grade_create = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grade_create",
    summary="Grade a homework submission",
    description="Create a grade for a homework submission. User must be a teacher or helper in the course.",
    request=GradeSerializer,
    responses={
        201: GradeSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_grade_update = extend_schema(
    tags=["Grades - Teacher"],
    operation_id="teacher_grade_update",
    summary="Update a grade",
    description="Update an existing grade for a homework submission. User must be a teacher or helper in the course.",
    request=GradeSerializer,
    responses={
        200: GradeSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)


student_grades_list = extend_schema(
    tags=["Grades - Student"],
    operation_id="student_grades_list",
    summary="List student's grades",
    description="Retrieve all grades for the authenticated student's submissions.",
    responses={
        200: GradeSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)
