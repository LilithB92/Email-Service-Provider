from django.db import models


# Create your models here.
class Recipient(models.Model):
    """Модель для получателей рассылки (клиентов)"""

    # Поле для email с уникальностью
    email = models.CharField(max_length=255, unique=True)
    # Фамилия
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    # Комментарий
    post = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


