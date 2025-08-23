from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.grade.serializers import GradeSerializer
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


grade_comments_list = extend_schema(
    tags=["GradeComments"],
    operation_id="grade_comments_list",
    summary="List comments for a grade",
    description=(
        "Retrieve all comments for a specific grade. "
        "Student can view comments on their own grades, "
        "teachers and helpers can view comments on grades from their courses."
    ),
    responses={
        200: GradeSerializer(many=True),
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

grade_comment_create = extend_schema(
    tags=["GradeComments"],
    operation_id="grade_comment_create",
    summary="Add comment to a grade",
    description=(
        "Create a comment for a grade. Students can comment on their own grades, "
        "teachers and helpers can comment on grades from their courses."
    ),
    request=GradeSerializer,
    responses={
        201: GradeSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)
