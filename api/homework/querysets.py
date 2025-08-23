from content.models import Lecture, Homework
from api.lectures.querysets import get_teacher_lectures


def get_teacher_homework(teacher_profile, lecture_id=None):

    lectures = get_teacher_lectures(teacher_profile)

    filtered_lectures = lectures.filter(id=lecture_id)

    return Homework.objects.filter(lecture__in=filtered_lectures).select_related(
        "lecture"
    )
