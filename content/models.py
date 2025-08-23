from common.models import AbstractModel
from django.db import models
from django.conf import settings


class StudentProfile(AbstractModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    name = models.CharField(max_length=25)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]


class TeacherProfile(AbstractModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]


class Courses(AbstractModel):
    name = models.CharField(max_length=70)
    teacher = models.ForeignKey(
        TeacherProfile,
        related_name="courses",
        on_delete=models.CASCADE,
    )
    helpers = models.ManyToManyField(
        TeacherProfile,
        related_name="helper_courses",
        blank=True,
    )
    available = models.BooleanField(default=True)
    student = models.ManyToManyField(
        StudentProfile,
        related_name="courses",
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["available"]),
            models.Index(fields=["teacher", "available"]),
            models.Index(fields=["name"]),
        ]


class Lecture(AbstractModel):
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, related_name="lectures"
    )
    topic = models.CharField(max_length=200)
    presentation_file = models.FileField(upload_to="lectures/", blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["course"]),
        ]


class Homework(AbstractModel):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="homeworks"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["lecture"]),
        ]


class HomeWorkSubmission(AbstractModel):
    class Status(models.TextChoices):
        SUBMITED = "submited", "Submited"
        GRADED = "graded", "Graded"
        RESUBMITED = "resubmited", "Resubmited"

    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="submissions"
    )
    text_submission = models.TextField(blank=True, null=True)
    submitted_file = models.FileField(
        upload_to="homework_submissions", blank=True, null=True
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.SUBMITED
    )

    class Meta:
        unique_together = ["homework", "student"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["homework"]),
            models.Index(fields=["student"]),
            models.Index(fields=["status"]),
            models.Index(fields=["homework", "student"]),
            models.Index(fields=["student", "status"]),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.homework.title} ({self.status})"


class Grade(AbstractModel):
    submission = models.OneToOneField(
        HomeWorkSubmission,
        on_delete=models.CASCADE,
        related_name="grade",
    )
    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    graded = models.BooleanField(default=False)
    feedback = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.submission.student.name} - {self.submission.homework.title}: {self.points if self.points is not None else 'Not graded'}"

    class Meta:
        indexes = [
            models.Index(fields=["submission"]),
            models.Index(fields=["graded"]),
        ]


class GradeComment(AbstractModel):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grade_comments",
    )
    text = models.TextField()

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["grade"]),
            models.Index(fields=["author"]),
            models.Index(fields=["grade", "author"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.grade}"
