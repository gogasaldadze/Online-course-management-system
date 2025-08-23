from content.models import Grade
from django.db.models import Q


def get_student_grades(student_profile):
    return Grade.objects.filter(submission__student=student_profile)


def get_teachers_of_course(teacher_profile):
    return Grade.objects.filter(
        Q(submission__homework__lecture__course__teacher=teacher_profile)
        | Q(submission__homework__lecture__course__helpers__in=[teacher_profile])
    )
