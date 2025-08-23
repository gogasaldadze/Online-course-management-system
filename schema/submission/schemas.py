from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
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
    summary="List student's submissions",
    description="Retrieve all homework submissions made by the student.",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by submission status",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="homework",
            description="Filter by homework UUID",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course", description="Filter by course ID", required=False, type=int
        ),
    ],
    responses={
        200: HomeWorkSubmissionSerializer(many=True),
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

student_submission_create = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_create",
    summary="Submit homework",
    description="Create a new homework submission for a student.",
    request=HomeWorkSubmissionSerializer,
    responses={
        201: HomeWorkSubmissionSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

student_submission_resubmit = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_resubmit",
    summary="Resubmit homework",
    description="Update an existing homework submission for resubmission.",
    request=HomeWorkSubmissionSerializer,
    responses={
        200: HomeWorkSubmissionSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

student_submission_retrieve = extend_schema(
    tags=["Submissions - Student"],
    operation_id="student_submission_retrieve",
    summary="Retrieve student submission",
    description="Retrieve detailed information about a specific homework submission.",
    responses={
        200: HomeWorkSubmissionSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)


teacher_submissions_list = extend_schema(
    tags=["Submissions - Teacher"],
    operation_id="teacher_submissions_list",
    summary="List submitted homework",
    description="Retrieve all homework submissions for courses where the user is a teacher.",
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by submission status",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="homework__title",
            description="Search by homework title",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="student__user__first_name",
            description="Filter by student first name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="student__user__last_name",
            description="Filter by student last name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="course", description="Filter by course ID", required=False, type=int
        ),
        OpenApiParameter(
            name="ordering",
            description="Order by field (e.g., created_at, -created_at)",
            required=False,
            type=str,
            enum=["created_at", "-created_at", "updated_at", "-updated_at"],
        ),
    ],
    responses={
        200: SubmittedHomeworkSerializer(many=True),
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_submission_retrieve = extend_schema(
    tags=["Submissions - Teacher"],
    operation_id="teacher_submission_retrieve",
    summary="Retrieve submission details",
    description="Retrieve detailed information about a specific homework submission for grading.",
    responses={
        200: SubmittedHomeworkSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)
