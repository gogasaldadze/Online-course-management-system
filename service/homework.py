from rest_framework.exceptions import NotFound
from content.models import Lecture, Homework


def teacher_create_homework(teacher_profile, lecture_id, data):
    try:
        lecture = Lecture.objects.for_teacher(teacher_profile).get(id=lecture_id)
    except Lecture.DoesNotExist:
        raise NotFound("Lecture not found or not owned by teacher")

    return Homework.objects.create(lecture=lecture, **data)


def teacher_update_homework(teacher_profile, lecture_id, homework_uuid, data):
    try:
        lecture = Lecture.objects.for_teacher(teacher_profile).get(id=lecture_id)
    except Lecture.DoesNotExist:
        raise NotFound("Lecture not found or not owned by teacher")

    try:
        existing_hw = Homework.objects.get(uuid=homework_uuid, lecture=lecture)
    except Homework.DoesNotExist:
        raise NotFound("Homework not found")

    # updating hw
    existing_hw.title = data.get("title", existing_hw.title)
    existing_hw.description = data.get("description", existing_hw.description)
    existing_hw.save()
    return existing_hw
