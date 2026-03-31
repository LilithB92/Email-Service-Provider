from django.contrib import admin

from mailing.models import Recipient


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "post")
    search_fields = ("full_name",)
