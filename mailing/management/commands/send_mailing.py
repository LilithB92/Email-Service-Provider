from django.core.management.base import BaseCommand

from mailing.services import SendMailing


class Command(BaseCommand):
    help = "Sends a mailing by ID"

    def add_arguments(self, parser):
        """Добавляет параметр mailing_id для командной строки"""
        parser.add_argument("mailing_id", type=int, help="ID of the mailing to send")

    def handle(self, *args, **options):
        """Отправление mailing через электронную почту"""
        mailing_id = options["mailing_id"]
        send_mailing = SendMailing()
        recipients = SendMailing.get_active_mailing_recipients(self=send_mailing, pk=mailing_id)
        for recipient in recipients:
            try:
                SendMailing.send_mailing(self=send_mailing, pk=mailing_id, recipient=recipient)
                # Запишите успешную попытку
                SendMailing.save_mailing_attempt(self=send_mailing, pk=mailing_id, status="success")
                self.stdout.write(self.style.SUCCESS(f'Successfully sent mailing "{mailing_id}"'))
            except Exception as e:
                SendMailing.save_mailing_attempt(self=send_mailing, pk=mailing_id, ex=e)
                # Запишите неудачную попытку
                self.stdout.write(
                    self.style.ERROR(f"Failed to send email to {recipient.email} for mailing {mailing_id}: {e}")
                )
