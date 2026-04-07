from django.contrib.auth import views as auth_views
from django.urls import path

from .apps import UsersConfig
from .forms import CustomAuthenticationForm
from .views import RegisterView

app_name = UsersConfig.name


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", form_class=CustomAuthenticationForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="users:login"), name="logout"),
]
