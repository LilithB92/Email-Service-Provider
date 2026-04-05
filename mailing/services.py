from django.utils import timezone

from mailing.models import Mailing
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
