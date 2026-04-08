import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm
from users.models import CustomUser


# Create your views here.
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
