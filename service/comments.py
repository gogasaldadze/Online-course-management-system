from rest_framework.exceptions import NotFound
from content.models import Grade, GradeComment


def list_comments(grade_uuid):
    try:
        grade = Grade.objects.get(uuid=grade_uuid)
    except Grade.DoesNotExist:
        raise NotFound("Grade not found.")
    return GradeComment.objects.filter(grade=grade)


def add_comment(grade_uuid, author, text):
    try:
        grade = Grade.objects.get(uuid=grade_uuid)
    except Grade.DoesNotExist:
        raise NotFound("Grade not found.")

    return GradeComment.objects.create(author=author, grade=grade, text=text)


