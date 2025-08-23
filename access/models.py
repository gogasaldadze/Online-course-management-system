from django.db import models

from common.models import AbstractModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from content.models import StudentProfile, TeacherProfile


class UserManager(BaseUserManager):
    def _create_user(self, username, password, role=None, name=None, **extra_fields):
        if not username:
            raise ValueError(("Username must be provided"))
        if not extra_fields.get("is_admin", False) and role not in [
            User.Roles.TEACHER,
            User.Roles.STUDENT,
        ]:
            raise ValueError("Role must be 'teacher' or 'student'")

        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if not extra_fields.get("is_admin", False):
            # Create related profile
            if role == User.Roles.TEACHER:
                TeacherProfile.objects.create(user=user, name=name)
            else:
                StudentProfile.objects.create(user=user, name=name)

        return user

    def create_user(self, username, password=None, role=None, **extra_fields):
        extra_fields.setdefault("is_admin", False)
        return self._create_user(username, password, role=role, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self._create_user(username, password, role=None, **extra_fields)


class User(AbstractBaseUser, AbstractModel):

    class Roles(models.TextChoices):
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    username = models.CharField(max_length=50, unique=True, db_index=True)
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        null=True,
        blank=True,
    )
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
