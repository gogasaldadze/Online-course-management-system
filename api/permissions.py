from rest_framework.permissions import BasePermission, SAFE_METHODS
from content.models import Grade, HomeWorkSubmission, GradeComment, Courses
from rest_framework.exceptions import NotFound


class AllowAny(BasePermission):

    def has_permission(self, request, view):
        return True


class IsTeacher(BasePermission):
    """Allow only authenticated teachers."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(
            request.user, "teacher_profile"
        )


class IsMainTeacher(BasePermission):
    """Object-level permission: only main teacher of the course can access."""

    def has_object_permission(self, request, view, obj):
        teacher_profile = getattr(request.user, "teacher_profile", None)
        if not teacher_profile:
            return False

        if isinstance(obj, Courses):
            return obj.teacher == teacher_profile

        if isinstance(obj, Grade):
            course = obj.submission.homework.lecture.course
        elif isinstance(obj, HomeWorkSubmission):
            course = obj.homework.lecture.course
        else:
            course = getattr(obj, "course", None)

        return course and course.teacher == teacher_profile


class IsHelper(BasePermission):
    """Object-level permission: course helpers or main teacher."""

    def has_object_permission(self, request, view, obj):
        teacher_profile = getattr(request.user, "teacher_profile", None)
        if not teacher_profile:
            return False

        if isinstance(obj, Grade):
            course = obj.submission.homework.lecture.course
        elif isinstance(obj, HomeWorkSubmission):
            course = obj.homework.lecture.course
        else:
            course = getattr(obj, "course", None)

        if not course:
            return False

        # Main teacher always allowed
        if course.teacher == teacher_profile:
            return True

        # Helpers allowed for safe methods and creating/updating grades/submissions
        if teacher_profile in course.helpers.all():
            if request.method in SAFE_METHODS:
                return True
            if isinstance(obj, (Grade, HomeWorkSubmission)):
                return True

        return False


class CanCommentGrade(BasePermission):
    """
    only allow commenting if:
    - The user is the student who owns the submission
    - OR the user is the main teacher of the course
    - OR the user is a helper of the course

    only allow viewing comments if:
    - The user meets any of the above conditions
    """

    def has_permission(self, request, view):
        grade_uuid = view.kwargs.get("grade_uuid")
        try:
            grade = Grade.objects.get(uuid=grade_uuid)
        except Grade.DoesNotExist:
            raise NotFound("Grade not found.")

        # For both GET and POST requests
        return self.has_object_permission(request, view, grade)

    def has_object_permission(self, request, view, obj):
        # If obj is GradeComment, check its parent Grade
        grade = obj.grade if isinstance(obj, GradeComment) else obj

        user = request.user
        teacher_profile = getattr(user, "teacher_profile", None)
        student_profile = getattr(user, "student_profile", None)

        course = grade.submission.homework.lecture.course

        # Student who owns the submission
        if student_profile and grade.submission.student == student_profile:
            return True

        # Main teacher
        if teacher_profile and course.teacher == teacher_profile:
            return True

        # Helper
        if teacher_profile and teacher_profile in course.helpers.all():
            return True

        return False
