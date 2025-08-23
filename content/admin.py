from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    StudentProfile,
    TeacherProfile,
    Courses,
    Lecture,
    Homework,
    HomeWorkSubmission,
    Grade,
    GradeComment,
)
from access.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["username"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    list_display = [
        "username",
        "get_name",
        "get_role",
        "is_admin",
        "created_at",
    ]
    list_filter = ["is_admin", "created_at", "role"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_select_related = ["student_profile", "teacher_profile"]

    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
        ("Additional Info", {"fields": ("uuid", "id", "role")}),
    )

    def get_name(self, obj):
        if obj.role == "teacher" and hasattr(obj, "teacher_profile"):
            return obj.teacher_profile.name
        elif obj.role == "student" and hasattr(obj, "student_profile"):
            return obj.student_profile.name
        return "-"

    get_name.short_description = "Name"

    def get_role(self, obj):
        return obj.role.capitalize() if obj.role else "-"

    get_role.short_description = "Role"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user_link", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "user__username"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at", "user_link"]
    raw_id_fields = ["user"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def user_link(self, obj):
        url = reverse("admin:access_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user_link", "courses_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "user__username"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at", "user_link"]
    raw_id_fields = ["user"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def user_link(self, obj):
        url = reverse("admin:access_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"

    def courses_count(self, obj):
        return obj.courses.count()

    courses_count.short_description = "Courses"


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ["name", "teacher", "available", "students_count", "created_at"]
    list_filter = ["available", "created_at"]
    search_fields = ["name", "teacher__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["teacher", "helpers"]
    filter_horizontal = ["student"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def students_count(self, obj):
        return obj.student.count()

    students_count.short_description = "Students"


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["topic", "course", "created_at"]
    list_filter = ["course", "created_at"]
    search_fields = ["topic", "course__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["course"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["title", "lecture", "submissions_count", "created_at"]
    list_filter = ["lecture__course", "created_at"]
    search_fields = ["title", "lecture__topic"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["lecture"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def submissions_count(self, obj):
        return obj.submissions.count()

    submissions_count.short_description = "Submissions"


@admin.register(HomeWorkSubmission)
class HomeWorkSubmissionAdmin(admin.ModelAdmin):
    list_display = ["homework", "student", "status", "created_at"]
    list_filter = ["status", "homework__lecture__course", "created_at"]
    search_fields = ["student__name", "homework__title"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["homework", "student"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["submission", "points", "graded", "created_at"]
    list_filter = ["graded", "submission__homework__lecture__course", "created_at"]
    search_fields = ["submission__student__name", "submission__homework__title"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["submission"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


@admin.register(GradeComment)
class GradeCommentAdmin(admin.ModelAdmin):
    list_display = ["grade", "author", "created_at"]
    list_filter = ["grade__submission__homework__lecture__course", "created_at"]
    search_fields = ["author__username", "grade__submission__student__name"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    raw_id_fields = ["grade", "author"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
