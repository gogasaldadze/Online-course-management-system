from django.urls import path, include
from .views import RegisterView, LogoutView


urlpatterns = [
    path("token/", include("api.auth.token.urls")),
    path("register/", RegisterView.as_view()),
    path(
        "logout/",
        LogoutView.as_view(),
    ),
]
