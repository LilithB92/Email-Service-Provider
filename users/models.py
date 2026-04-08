from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, help_text="Введите Ваша почта")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Введите Ваш номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    country = models.CharField(max_length=60, blank=True, null=True, help_text="Введите Ваша страна")
    token = models.CharField(
        max_length=100,
        verbose_name="Token",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email
