from rest_framework.exceptions import ValidationError, PermissionDenied
from content.models import Homework, HomeWorkSubmission, StudentProfile


def create_submission(homework_uuid, student_profile, data):
    if not homework_uuid:
        raise ValidationError({"homework": "Homework UUID is required."})

    try:
        homework = Homework.objects.get(uuid=homework_uuid)
    except Homework.DoesNotExist:
        raise ValidationError({"homework": "Invalid homework UUID"})

    if HomeWorkSubmission.objects.filter(homework=homework, student=student_profile).exists():
        raise ValidationError({"homework": "You have already submitted this homework."})

    return HomeWorkSubmission.objects.create(
        student=student_profile,
        homework=homework,
        status=HomeWorkSubmission.Status.SUBMITED,
        **data
    )


def resubmit_submission(submission_uuid, student_profile, data):
    try:
        existing = HomeWorkSubmission.objects.get(student=student_profile, uuid=submission_uuid)
    except HomeWorkSubmission.DoesNotExist:
        raise ValidationError({"Submission": "Invalid homework submission UUID"})

    # Update existing submission for resubmission
    existing.text_submission = data.get('text_submission', existing.text_submission)
    existing.submitted_file = data.get('submitted_file', existing.submitted_file)
    existing.status = HomeWorkSubmission.Status.RESUBMITED
    existing.save()
    return existing
