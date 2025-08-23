from content.models import HomeWorkSubmission
from django.db.models import Q


def get_homework_submission(student_profile):
    return HomeWorkSubmission.objects.filter(student=student_profile)


def get_teachers_of_course(teacher_profile):

    return HomeWorkSubmission.objects.filter(
        Q(homework__lecture__course__teacher=teacher_profile)
        | Q(homework__lecture__course__helpers__in=[teacher_profile])
    )
