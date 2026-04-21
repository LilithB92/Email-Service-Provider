from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView
from django.urls import path
from django.urls import reverse_lazy

from .apps import UsersConfig
from .forms import CustomAuthenticationForm
from .views import BlockUserView
from .views import ConfirmationEmailView
from .views import CustomUserList
from .views import ProfileDetailView
from .views import ProfileUpdateView
from .views import RegisterView
from .views import logout_view

app_name = UsersConfig.name


urlpatterns = [
    path("customuser_list/", CustomUserList.as_view(), name="custom_user_list"),
    path("customuser_block/<int:pk>/", BlockUserView.as_view(), name="custom_user_block"),
    path("profile/update/<int:pk>/", ProfileUpdateView.as_view(), name="profile_update"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", form_class=CustomAuthenticationForm),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("email_confirm/<str:token>/", ConfirmationEmailView.as_view(), name="email_confirm"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
