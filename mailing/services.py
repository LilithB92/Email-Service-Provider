from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailing.models import Mailing, MailingAttempt
from mailing.models import Recipient


class MailingRecipientService:

    @staticmethod
    def count_mailings():
        """Общее количество всех созданных рассылок"""
        count_mailings = Mailing.objects.count()
        return count_mailings

    @staticmethod
    def count_recipients():
        """Количество уникальных получателей (общее число клиентов в системе)"""
        count_recipients = Recipient.objects.count()
        return count_recipients

    @staticmethod
    def active_mailings_count():
        """Количество активных рассылок"""
        current_time = timezone.now()
        active_mailings_count = Mailing.objects.filter(
            start_time__lte=current_time, end_time__gte=current_time
        ).count()
        return active_mailings_count


class SendMailing:
    """Отправление рассылок"""

    @staticmethod
    def get_active_mailing(pk):
        """ Получаем активного рассылка"""
        current_time = timezone.now()
        active_mailing =Mailing.objects.get(
            start_time__lte=current_time, end_time__gte=current_time, pk=pk
        )
        return  active_mailing

    def get_active_mailing_recipients(self, pk):
        """Получаем список получателей(object) активного рассылка"""
        mailing = self.get_active_mailing(pk)
        recipients = mailing.recipients.all()
        return recipients

    def send_mailing(self, pk, recipient):
        mailing = self.get_active_mailing(pk=pk)
        send_mail(
            mailing.message.subject,
            mailing.message.text,
            settings.EMAIL_HOST_USER,  # Отправляем письмо
            [recipient.email],  # Электронное письмо получателя
            fail_silently=False,
        )

    def save_mailing_attempt(self, pk:int, status:str='failure', ex: object=None)->None:
        """Сохраняет попыток отправки электронных почт в DB"""
        mailing = self.get_active_mailing(pk)
        if status == 'success':
            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response="Email sent successfully",
            )
            # При необходимости обновите статус рассылки
            mailing.status = "completed"
            mailing.save()
        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=str(ex))


class MailingAttemptService:

    @staticmethod
    def get_mailing_attempts_count():
        """"""
        return MailingAttempt.objects.count()

    @staticmethod
    def get_success_attempts_count():
        return MailingAttempt.objects.filter(status="success").count()
