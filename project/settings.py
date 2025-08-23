from pathlib import Path
import dj_database_url
from project.environment import ENV
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = ENV.str("SECRET_KEY")


DEBUG = ENV.bool("DEBUG")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "common.apps.CommonConfig",
    "content.apps.ContentConfig",
    "access.apps.AccessConfig",
    "api.apps.ApiConfig",
    # for scripts
    "django_extensions",
    # drf
    "rest_framework",
    # JWT
    "rest_framework_simplejwt.token_blacklist",
    # doccumentation
    "drf_spectacular",
    # optimization tracking
    "silk",
    # filters
    "django_filters",
]

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config()
}  # i rly dont like exposing postgre creds even with env variables


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "access.User"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 2,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "api.throttles.BurstRateThrottle",
        "api.throttles.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/min",
        "burst": "15/min",
        "sustained": "150/hour",
    },
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=ENV.int("AUTH_JWT_ACCESS_TOKEN_TIMEOUT", default=86400)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=ENV.int("AUTH_JWT_REFRESH_TOKEN_TIMEOUT", default=604800)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": ENV.str("AUTH_JWT_SIGNING_KEY"),
    "USER_ID_FIELD": "uuid",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Online course management system",
    "DESCRIPTION": "API for courses, lectures, homework, submissions, grades, and comments.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    "TAGS": [
        {"name": "Authentication", "description": "User authentication endpoints"},
        {"name": "Courses - Teacher", "description": "Course management for teachers"},
        {"name": "Courses - Student", "description": "Course management for students"},
        {
            "name": "Lectures - Teacher",
            "description": "Lecture management for teachers",
        },
        {"name": "Lectures - Student", "description": "Lecture access for students"},
        {
            "name": "Homework - Teacher",
            "description": "Homework assignment management for teachers",
        },
        {"name": "Homework - Student", "description": "Homework access for students"},
        {
            "name": "Submissions - Teacher",
            "description": "Submission management for teachers",
        },
        {
            "name": "Submissions - Student",
            "description": "Submission management for students",
        },
        {"name": "Grades - Teacher", "description": "Grading management for teachers"},
        {"name": "Grades - Student", "description": "Grade access for students"},
        {"name": "GradeComments", "description": "Comments on grades"},
    ],
}
