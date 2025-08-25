from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.submission.serializers import (
    HomeWorkSubmissionSerializer,
    SubmittedHomeworkSerializer,
)
from schema.serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


student_submissions_list = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submissions_list",
    summary="List student submissions",
    description="Get student's homework submissions",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Submission status",
            required=False,
            type=str,
            enum=["pending", "submitted", "graded"],
        ),
        OpenApiParameter(
            name="homework_uuid",
            description="Homework UUID",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course",
            description="Course ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: HomeWorkSubmissionSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


student_submission_create = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_create",
    summary="Submit homework",
    description="Submit homework assignment",
    request=HomeWorkSubmissionSerializer,
    responses={
        201: HomeWorkSubmissionSerializer,
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


student_submission_resubmit = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_resubmit",
    summary="Resubmit homework",
    description="Resubmit homework assignment",
    request=HomeWorkSubmissionSerializer,
    responses={
        200: HomeWorkSubmissionSerializer,
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


student_submission_retrieve = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_retrieve",
    summary="Get submission details",
    description="Get specific homework submission",
    responses={
        200: HomeWorkSubmissionSerializer,
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


teacher_submissions_list = extend_schema(
    tags=["Submissions - Teacher"],
    operation_id="teacher_submissions_list",
    summary="List homework submissions",
    description="Get homework submissions for teacher's courses",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Submission status",
            required=False,
            type=str,
            enum=["pending", "submitted", "graded"],
        ),
        OpenApiParameter(
            name="student_first_name",
            description="Student first name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="student_last_name",
            description="Student last name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course",
            description="Course ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: SubmittedHomeworkSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_submission_retrieve = extend_schema(
    tags=["Submissions - Teacher"],
    operation_id="teacher_submission_retrieve",
    summary="Get submission details",
    description="Get specific homework submission",
    responses={
        200: SubmittedHomeworkSerializer,
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
