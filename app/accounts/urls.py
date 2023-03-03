from django.urls import path

from .views import UserPasswordChangeView, UsersEmailVerify, UsersMeView, UsersView

urlpatterns = [
    path("users/", UsersView.as_view(), name="users"),
    path("users/me/", UsersMeView.as_view(), name="users_me"),
    path(
        "users/me/password_change/",
        UserPasswordChangeView.as_view(),
        name="users_me_password_change",
    ),
    path(
        "users/email/<str:email>/",
        UsersEmailVerify.as_view(),
        name="users_email_verify",
    ),
]
