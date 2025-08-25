# schema/courses/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.courses.serializers import (
    ListCoursesTeacherSerializer,
    ListCoursesStudentSerializer,
    CreateCoursesSerializer,
    UpdateCoursesSerializer,
    StudentRegisteredCoursesSerializer,
)
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


teacher_courses_list = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_courses_list",
    summary="List teacher courses",
    description="Get courses where user is main teacher",
    parameters=[
        OpenApiParameter(
            name="name",
            description="Course name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="student_name",
            description="Student name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="helper_id",
            description="Helper ID",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: ListCoursesTeacherSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_course_create = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_create",
    summary="Create course",
    description="Create new course",
    request=CreateCoursesSerializer,
    responses={
        201: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


teacher_course_retrieve = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_retrieve",
    summary="Get course details",
    description="Get specific course details",
    responses={
        200: ListCoursesTeacherSerializer,
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


teacher_course_update = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_update",
    summary="Update course",
    description="Update course details",
    request=UpdateCoursesSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
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


teacher_course_partial_update = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_partial_update",
    summary="Partial update course",
    description="Partially update course details",
    request=UpdateCoursesSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
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


teacher_course_delete = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_delete",
    summary="Delete course",
    description="Delete course",
    responses={
        204: None,
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


student_courses_available_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_available_list",
    summary="List available courses",
    description="Get courses available for enrollment",
    parameters=[
        OpenApiParameter(
            name="name",
            description="Course name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="teacher_name",
            description="Teacher name",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: ListCoursesStudentSerializer(many=True),
    },
)


student_courses_registered_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_registered_list",
    summary="List registered courses",
    description="Get courses where student is enrolled",
    parameters=[
        OpenApiParameter(
            name="name",
            description="Course name",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="teacher_name",
            description="Teacher name",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: StudentRegisteredCoursesSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Authentication required",
        ),
    },
)


student_course_registered_retrieve = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_course_registered_retrieve",
    summary="Get registered course",
    description="Get specific registered course details",
    responses={
        200: StudentRegisteredCoursesSerializer,
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
