from django.urls import path, include


urlpatterns = [
    path("auth/", include("api.auth.urls")),
    path("courses/", include("api.courses.urls")),
    path("homeworks/", include("api.homework.urls")),
]
