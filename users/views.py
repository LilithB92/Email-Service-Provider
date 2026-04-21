import secrets

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm
from users.models import CustomUser

# Create your views here.
User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")  # Redirect to the 'login' URL name
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}"
        self.send_welcome_email(user, url)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, url):
        subject = "Подтверждение почты"
        message = f"Привет, перейти по ссылке для подтверждения почты {url}"
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class ConfirmationEmailView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, token=token)
        user.is_active = True
        user.save()
        return redirect(reverse("users:login"))


class ProfileDetailView(DetailView):
    model = CustomUser


def logout_view(request):
    logout(request)
    return redirect(reverse("users:login"))


class BlockUserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        if not request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")
        user.is_active = False
        user.save()
        return redirect(reverse("users:custom_user_list"))


class CustomUserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    context_object_name = "users"
    paginate_by = 2
    permission_required = "users.view_customuser"
