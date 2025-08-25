from content.models import Courses, StudentProfile, TeacherProfile, Notification
from rest_framework.exceptions import ValidationError


def create_course_with_students(teacher, name, available=True, student_ids=None):
    student_ids = student_ids or []
    course = Courses.objects.create(name=name, available=available, teacher=teacher)
    if student_ids:
        students = StudentProfile.objects.filter(id__in=student_ids)
        found_ids = set(students.values_list("id", flat=True))
        missing = [sid for sid in student_ids if sid not in found_ids]
        if missing:
            raise ValidationError({"student_ids": f"Invalid IDs: {missing}"})
        course.student.add(*students)
        for s in students:
            Notification.objects.create(
                user=s.user,
                title="Course enrollment",
                message=f"You have been enrolled in course '{course.name}'.",
            )
    return course


def update_course_students(course, add_ids=None, remove_ids=None):
    add_ids = add_ids or []
    remove_ids = remove_ids or []
    if add_ids:
        students = StudentProfile.objects.filter(id__in=add_ids)
        found_ids = set(students.values_list("id", flat=True))
        missing = [sid for sid in add_ids if sid not in found_ids]
        if missing:
            raise ValidationError({"student_add_ids": f"Invalid IDs: {missing}"})
        course.student.add(*students)
        for s in students:
            Notification.objects.create(
                user=s.user,
                title="Course enrollment",
                message=f"You have been added to course '{course.name}'.",
            )
    if remove_ids:
        students = StudentProfile.objects.filter(id__in=remove_ids)
        found_ids = set(students.values_list("id", flat=True))
        missing = [sid for sid in remove_ids if sid not in found_ids]
        if missing:
            raise ValidationError({"student_remove_ids": f"Invalid IDs: {missing}"})
        course.student.remove(*students)
    return course


def manage_helpers(course, add_ids=None, remove_ids=None):
    add_ids = add_ids or []
    remove_ids = remove_ids or []
    if add_ids:
        helpers = TeacherProfile.objects.filter(id__in=add_ids)
        found_ids = set(helpers.values_list("id", flat=True))
        missing = [hid for hid in add_ids if hid not in found_ids]
        if missing:
            raise ValidationError({"helpers_add_ids": f"Invalid IDs: {missing}"})
        course.helpers.add(*helpers)
    if remove_ids:
        helpers = TeacherProfile.objects.filter(id__in=remove_ids)
        found_ids = set(helpers.values_list("id", flat=True))
        missing = [hid for hid in remove_ids if hid not in found_ids]
        if missing:
            raise ValidationError({"helpers_remove_ids": f"Invalid IDs: {missing}"})
        course.helpers.remove(*helpers)
    return course


