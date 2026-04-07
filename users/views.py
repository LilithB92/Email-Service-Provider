from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CustomUserCreationForm


# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")  # Redirect to the 'login' URL name
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)

        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = 'LilithBich@yandex.ru'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)