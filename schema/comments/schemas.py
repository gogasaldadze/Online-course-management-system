from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.comments.serializers import GradeCommentSerializer
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


grade_comments_list = extend_schema(
    tags=["Comments"],
    operation_id="grade_comments_list",
    summary="List grade comments",
    description="Get comments for specific grade",
    responses={
        200: GradeCommentSerializer(many=True),
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


grade_comment_create = extend_schema(
    tags=["Comments"],
    operation_id="grade_comment_create",
    summary="Create comment",
    description="Add comment to grade",
    request=GradeCommentSerializer,
    responses={
        201: GradeCommentSerializer,
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
