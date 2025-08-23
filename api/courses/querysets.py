# api/courses/query_helpers.py
from django.db.models import Prefetch, Count
from content.models import Courses, Lecture, TeacherProfile, StudentProfile


def get_available_courses():
    return (
        Courses.objects.filter(available=True)
        .select_related("teacher")
        .prefetch_related(
            Prefetch(
                "lectures",
                queryset=Lecture.objects.only("id", "topic", "course_id"),
                to_attr="prefetched_lectures",
            ),
        )
        .only("id", "name", "teacher_id")
    )


def get_all_courses():

    return (
        Courses.objects.all()
        .select_related("teacher")
        .prefetch_related(
            Prefetch("lectures", queryset=Lecture.objects.only("id", "topic")),
            Prefetch("helpers", queryset=TeacherProfile.objects.only("id", "name")),
            Prefetch("student", queryset=StudentProfile.objects.only("id", "name")),
        )
        .only("id", "name", "teacher_id")
    )


def get_all_courses_helper():
    return (
        Courses.objects.filter(available=True)
        .select_related("teacher")
        .prefetch_related(
            Prefetch(
                "lectures",
                queryset=Lecture.objects.only("id", "topic", "course_id"),
                to_attr="prefetched_lectures",
            ),
            Prefetch(
                "helpers",
                queryset=TeacherProfile.objects.only("id", "name"),
                to_attr="prefetched_helpers",
            ),
            Prefetch(
                "student",
                queryset=StudentProfile.objects.only("id", "name"),
                to_attr="prefetched_students",
            ),
        )
        .only("id", "name", "teacher_id", "uuid")
    )


def get_teacher_courses_optimized(teacher_profile):

    return (
        Courses.objects.filter(teacher=teacher_profile)
        .select_related("teacher")
        .prefetch_related(
            Prefetch(
                "helpers",
                queryset=TeacherProfile.objects.only("id", "name"),
            ),
            Prefetch("student", queryset=StudentProfile.objects.only("id", "name")),
        )
        .annotate(student_quantity=Count("student", distinct=True))
        .only(
            "id",
            "uuid",
            "name",
            "teacher",
            "student",
            "helpers",
        )
    )


def get_student_courses_optimized(student_profile):
    return (
        Courses.objects.filter(student=student_profile)
        .select_related("teacher")
        .only("id", "name", "teacher_id", "uuid", "created_at")
    )
