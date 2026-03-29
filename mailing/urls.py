from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import RecipientList

app_name = MailingConfig.name

urlpatterns = [
    path("recipient/", RecipientList.as_view(), name="recipient_list"),
]
