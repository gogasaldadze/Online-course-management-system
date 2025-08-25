from rest_framework.exceptions import PermissionDenied, NotFound
from content.models import Grade, HomeWorkSubmission


def create_grade(submission_uuid, teacher_profile, data):
    try:
        submission = HomeWorkSubmission.objects.get(uuid=submission_uuid)
    except HomeWorkSubmission.DoesNotExist:
        raise NotFound("Submission not found.")

    if Grade.objects.filter(submission=submission).exists():
        raise PermissionDenied("Grade already exists. Use update.")

    grade = Grade.objects.create(submission=submission, graded=True, **data)
    submission.status = HomeWorkSubmission.Status.GRADED
    submission.save()
    return grade


def update_grade(submission_uuid, teacher_profile, data):
    try:
        submission = HomeWorkSubmission.objects.get(uuid=submission_uuid)
    except HomeWorkSubmission.DoesNotExist:
        raise NotFound("Submission not found.")

    try:
        existing_grade = Grade.objects.get(submission=submission)
    except Grade.DoesNotExist:
        raise NotFound("Grade does not exist. Create it first.")

    # Update existing grade
    existing_grade.points = data.get('points', existing_grade.points)
    existing_grade.feedback = data.get('feedback', existing_grade.feedback)
    existing_grade.graded = True
    existing_grade.save()

    submission.status = HomeWorkSubmission.Status.GRADED
    submission.save()
    return existing_grade


