from django.db import models
from django.db.models import Prefetch, Count
from django.apps import apps
from django.db.models import Q


# Course
class CoursesQuerySet(models.QuerySet):
    def is_available(self):
        return self.filter(available=True)

    def with_teacher(self):
        return self.select_related("teacher")

    def with_lectures(self):
        Lecture = apps.get_model("content", "Lecture")
        return self.prefetch_related(
            Prefetch(
                "lectures",
                queryset=Lecture.objects.only("id", "topic", "course_id"),
                to_attr="prefetched_lectures",
            )
        )

    def with_helpers(self):
        TeacherProfile = apps.get_model("content", "TeacherProfile")
        return self.prefetch_related(
            Prefetch("helpers", queryset=TeacherProfile.objects.only("id", "name"))
        )

    def with_students(self):
        StudentProfile = apps.get_model("content", "StudentProfile")
        return self.prefetch_related(
            Prefetch("student", queryset=StudentProfile.objects.only("id", "name"))
        )

    def only_basic(self):
        return self.only("id", "name", "teacher_id")

    def for_teacher_optimized(self, teacher_profile):
        StudentProfile = apps.get_model("content", "StudentProfile")
        return (
            self.filter(teacher=teacher_profile)
            .with_teacher()
            .with_helpers()
            .prefetch_related(
                Prefetch("student", queryset=StudentProfile.objects.only("id", "name"))
            )
            .annotate(student_quantity=Count("student", distinct=True))
            .only("id", "uuid", "name", "teacher", "student", "helpers")
        )

    def for_student_optimized(self, student_profile):
        return (
            self.filter(student=student_profile)
            .with_teacher()
            .only("id", "name", "teacher_id", "uuid", "created_at")
        )


class CoursesManager(models.Manager):
    def get_queryset(self):
        return CoursesQuerySet(self.model, using=self._db)

    def is_available(self):
        return self.get_queryset().is_available()

    def with_teacher(self):
        return self.get_queryset().with_teacher()

    def with_lectures(self):
        return self.get_queryset().with_lectures()

    def with_helpers(self):
        return self.get_queryset().with_helpers()

    def with_students(self):
        return self.get_queryset().with_students()

    def only_basic(self):
        return self.get_queryset().only_basic()

    def for_teacher_optimized(self, teacher_profile):
        return self.get_queryset().for_teacher_optimized(teacher_profile)

    def for_student_optimized(self, student_profile):
        return self.get_queryset().for_student_optimized(student_profile)

    def all_with_related_basic(self):
        return (
            self.get_queryset()
            .with_teacher()
            .with_lectures()
            .with_helpers()
            .with_students()
            .only_basic()
        )


# Lectures
class LectureQuerySet(models.QuerySet):
    def for_teacher(self, teacher_profile):
        return (
            self.filter(course__teacher=teacher_profile)
            .select_related("course__teacher")
            .prefetch_related("course__student")
            .only(
                "id",
                "uuid",
                "created_at",
                "updated_at",
                "course_id",
                "topic",
                "presentation_file",
            )
        )

    def for_student(self, student_profile):
        return (
            self.filter(course__student=student_profile)
            .select_related("course__teacher")
            .only("id", "topic", "presentation_file", "course_id")
        )


class LectureManager(models.Manager):
    def get_queryset(self):
        return LectureQuerySet(self.model, using=self._db)

    def for_teacher(self, teacher_profile):
        return self.get_queryset().for_teacher(teacher_profile)

    def for_student(self, student_profile):
        return self.get_queryset().for_student(student_profile)


# Homework
class HomeworkQuerySet(models.QuerySet):
    def for_teacher(self, teacher_profile, lecture_id=None):
        qs = self.filter(lecture__course__teacher=teacher_profile)
        if lecture_id is not None:
            qs = qs.filter(lecture_id=lecture_id)
        return qs.select_related("lecture")

    def for_teacher_all(self, teacher_profile):
        return self.filter(lecture__course__teacher=teacher_profile)

    def for_student(self, student_profile):
        return self.filter(lecture__course__student=student_profile)


class HomeworkManager(models.Manager):
    def get_queryset(self):
        return HomeworkQuerySet(self.model, using=self._db)

    def for_teacher(self, teacher_profile, lecture_id=None):
        return self.get_queryset().for_teacher(teacher_profile, lecture_id)

    def for_teacher_all(self, teacher_profile):
        return self.get_queryset().for_teacher_all(teacher_profile)

    def for_student(self, student_profile):
        return self.get_queryset().for_student(student_profile)


# Submissions
class HomeWorkSubmissionQuerySet(models.QuerySet):
    def for_student(self, student_profile):
        return self.filter(student=student_profile)

    def for_teachers_of_course(self, teacher_profile):

        return self.filter(
            Q(homework__lecture__course__teacher=teacher_profile)
            | Q(homework__lecture__course__helpers__in=[teacher_profile])
        )


class HomeWorkSubmissionManager(models.Manager):
    def get_queryset(self):
        return HomeWorkSubmissionQuerySet(self.model, using=self._db)

    def for_student(self, student_profile):
        return self.get_queryset().for_student(student_profile)

    def for_teachers_of_course(self, teacher_profile):
        return self.get_queryset().for_teachers_of_course(teacher_profile)


# Grades
class GradeQuerySet(models.QuerySet):
    def for_student(self, student_profile):
        return self.filter(submission__student=student_profile)

    def for_teachers_of_course(self, teacher_profile):

        return self.filter(
            Q(submission__homework__lecture__course__teacher=teacher_profile)
            | Q(submission__homework__lecture__course__helpers__in=[teacher_profile])
        )


class GradeManager(models.Manager):
    def get_queryset(self):
        return GradeQuerySet(self.model, using=self._db)

    def for_student(self, student_profile):
        return self.get_queryset().for_student(student_profile)

    def for_teachers_of_course(self, teacher_profile):
        return self.get_queryset().for_teachers_of_course(teacher_profile)
