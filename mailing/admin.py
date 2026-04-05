from django.contrib import admin

from mailing.models import Mailing
from mailing.models import MailingAttempt
from mailing.models import Message
from mailing.models import Recipient


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "post")
    search_fields = ("full_name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "text")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "message")


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ("mailing", "attempt_time", "status", "server_response")
    list_filter = ("status",)
    search_fields = ("attempt_time",)
