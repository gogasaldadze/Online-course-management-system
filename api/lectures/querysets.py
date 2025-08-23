from content.models import Lecture
from api.courses.querysets import get_student_courses_optimized


def get_student_lectures(student_profile):
    """
    Returns all lectures for courses that the given student is enrolled in.
    """
    courses = get_student_courses_optimized(student_profile)
    return (
        Lecture.objects.filter(course__in=courses)
        .select_related("course__teacher")
        .only("id", "topic", "presentation_file", "course_id")
    )


def get_teacher_lectures(teacher_profile):
    """
    Returns all lectures for courses that the given teacher teaches.
    """
    return (
        Lecture.objects.filter(course__teacher=teacher_profile)
        .select_related("course__teacher")
        .prefetch_related("course__student")
        .only(
            "id",
            "uuid",
            "created_at",
            "updated_at",
            "course_id",
            "topic",
            "presentation_file",
        )
    )


ALL_LECTURES = Lecture.objects.all()
