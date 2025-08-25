from rest_framework.exceptions import NotFound, PermissionDenied
from content.models import Courses, Lecture


def teacher_create_lecture(teacher_profile, course_id, data):
    try:
        course = Courses.objects.get(id=course_id, teacher=teacher_profile)
    except Courses.DoesNotExist:
        raise NotFound("Course not found or not owned by teacher")

    return Lecture.objects.create(course=course, **data)


