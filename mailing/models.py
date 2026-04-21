from django.db import models

from users.models import CustomUser


# Create your models here.
class Recipient(models.Model):
    """Модель для получателей рассылки (клиентов)"""

    # Поле для email с уникальностью
    email = models.CharField(max_length=255, unique=True)
    # Фамилия
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    # Комментарий
    post = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    # Владелец
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="owner")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["pk"]


class Message(models.Model):
    """Модель для сообщения"""

    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Тело письма")
    # Владелец
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="owner")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    """Модель для рассылки"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
    ]
    start_time = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="message")
    recipients = models.ManyToManyField(Recipient, verbose_name="recipients")
    # Владелец
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="owner")

    def __str__(self):
        return f"Рассылка {self.pk}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [("can_disable_mailing", "Can disable mailing")]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failure", "Не успешно"),
    ]
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="mailing")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(null=True, blank=True, verbose_name="Ответ почтового сервера")

    def _str_(self):
        return f"Попытка рассылки {self.mailing.pk} - {self.attempt_time}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
