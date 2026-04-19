from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from config import settings
from mailing.models import Mailing
from mailing.models import MailingAttempt


class Command(BaseCommand):
    help = "Sends a mailing by ID"

    def add_arguments(self, parser):
        """Добавляет параметр mailing_id для командной строки"""
        parser.add_argument("mailing_id", type=int, help="ID of the mailing to send")

    def handle(self, *args, **options):
        """Отправление mailing через электронную почту"""
        mailing_id = options["mailing_id"]
        mailing = Mailing.objects.get(pk=mailing_id)
        recipients = mailing.recipients.all()
        if mailing.status == "completed":
            self.stdout.write(self.style.SUCCESS(f'Mailing with pk "{mailing.pk}" is already completed'))
        else:
            # Привлекаем клиентов для рассылки
            for recipient in recipients:
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.text,
                        settings.EMAIL_HOST_USER,  # Отправляем письмо
                        [recipient.email],  # Электронное письмо получателя
                        fail_silently=False,
                    )
                    # Запишите успешную попытку
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status="success",
                        server_response="Email sent successfully",
                    )
                    # # При необходимости обновите статус рассылки
                    mailing.status = "completed"
                    mailing.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully sent mailing "{mailing.pk}"'))
                except Exception as e:
                    # Запишите неудачную попытку
                    MailingAttempt.objects.create(mailing=mailing, status="failure", server_response=str(e))
                    self.stdout.write(
                        self.style.ERROR(f"Failed to send email to {recipient.email} for mailing {mailing.pk}: {e}")
                    )
