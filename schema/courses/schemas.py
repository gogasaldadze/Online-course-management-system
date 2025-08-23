# api/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.courses.serializers import (
    ListCoursesStudentSerializer,
    ListCoursesTeacherSerializer,
    CreateCoursesSerializer,
    UpdateCoursesSerializer,
    StudentRegisteredCoursesSerializer,
    AddHelperSerializer,
)
from ..serializers import (
    ValidationErrorSerializer,
    PermissionDeniedSerializer,
    NotFoundSerializer,
)


teacher_courses_list = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_courses_list",
    summary="List teacher's courses",
    description="Retrieve all courses where the authenticated user is the main teacher.",
    responses={
        200: ListCoursesTeacherSerializer(many=True),
        403: PermissionDeniedSerializer,
    },
)

teacher_course_create = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_create",
    summary="Create a new course",
    description="Create a new course with the authenticated user as the main teacher.",
    request=CreateCoursesSerializer,
    responses={
        201: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
    },
)

teacher_course_retrieve = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_retrieve",
    summary="Retrieve teacher's course details",
    description="Retrieve detailed information about a specific course where user is the main teacher.",
    responses={
        200: ListCoursesTeacherSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_course_update = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_update",
    summary="Update teacher's course",
    description="Full update of a course where user is the main teacher.",
    request=UpdateCoursesSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_course_partial_update = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_partial_update",
    summary="Partially update teacher's course",
    description="Partial update of a course where user is the main teacher.",
    request=UpdateCoursesSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

teacher_course_delete = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="teacher_course_delete",
    summary="Delete teacher's course",
    description="Delete a course where user is the main teacher.",
    responses={
        204: None,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)

manage_helpers = extend_schema(
    tags=["Courses - Teacher"],
    operation_id="course_manage_helpers",
    summary="Manage helper teachers for course",
    description="Add or remove helper teachers from a course. Only the main teacher (owner) can manage helpers.",
    request=AddHelperSerializer,
    responses={
        200: ListCoursesTeacherSerializer,
        400: ValidationErrorSerializer,
        403: PermissionDeniedSerializer,
        404: NotFoundSerializer,
    },
)


student_courses_available_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_available_list",
    summary="List available courses for enrollment",
    description="Retrieve all courses that are available for student enrollment.",
    responses={
        200: ListCoursesStudentSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - Authentication required",
        ),
    },
)

student_courses_registered_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_registered_list",
    summary="List student's registered courses",
    description="Retrieve all courses where the student is currently enrolled.",
    responses={
        200: StudentRegisteredCoursesSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - User is not a student",
        ),
    },
)

student_course_registered_retrieve = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_course_registered_retrieve",
    summary="Retrieve student's enrolled course details",
    description="Retrieve detailed information about a specific course where the student is enrolled.",
    responses={
        200: StudentRegisteredCoursesSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - User is not a student",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer, description="Course not found or not enrolled"
        ),
    },
)


student_courses_available_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_available_list",
    summary="List available courses for enrollment",
    description="Retrieve all courses that are available for student enrollment.",
    responses={
        200: ListCoursesStudentSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - Authentication required",
        ),
    },
)

student_courses_registered_list = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_courses_registered_list",
    summary="List student's registered courses",
    description="Retrieve all courses where the student is currently enrolled.",
    responses={
        200: StudentRegisteredCoursesSerializer(many=True),
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - User is not a student",
        ),
    },
)

student_course_registered_retrieve = extend_schema(
    tags=["Courses - Student"],
    operation_id="student_course_registered_retrieve",
    summary="Retrieve student's enrolled course details",
    description="Retrieve detailed information about a specific course where the student is enrolled.",
    responses={
        200: StudentRegisteredCoursesSerializer,
        403: OpenApiResponse(
            response=PermissionDeniedSerializer,
            description="Forbidden - User is not a student",
        ),
        404: OpenApiResponse(
            response=NotFoundSerializer, description="Course not found or not enrolled"
        ),
    },
)
