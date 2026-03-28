from django.db import models


# Create your models here.
class Client(models.Model):
    """Модель для получателей рассылки (клиентов)"""

    # Поле для email с уникальностью
    email = models.EmailField(max_length=255, unique=True, verbose_name="Почтовый адрес")
    # Фамилия
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    # Имя
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    # Отчество (необязательным)
    middle_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True, null=True)
    # Комментарий
    post = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
