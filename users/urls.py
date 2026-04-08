from django.contrib.auth import views as auth_views
from django.urls import path

from .apps import UsersConfig
from .forms import CustomAuthenticationForm
from .views import ConfirmationEmailView
from .views import CustomUserDetailView
from .views import RegisterView
from .views import logout_view

app_name = UsersConfig.name


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", form_class=CustomAuthenticationForm),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("email_confirm/<str:token>/", ConfirmationEmailView.as_view(), name="email_confirm"),
    path("profil/<int:pk>", CustomUserDetailView.as_view(), name="profil"),
]
