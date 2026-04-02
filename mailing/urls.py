from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MessageCreateView, MessageDeleteView
from mailing.views import MessageDetailView
from mailing.views import MessageList
from mailing.views import MessageUpdateView
from mailing.views import RecipientCreateView
from mailing.views import RecipientDeleteView
from mailing.views import RecipientDetailView
from mailing.views import RecipientList
from mailing.views import RecipientUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path("recipient/", RecipientList.as_view(), name="recipient_list"),
    path("recipient_detail/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/new/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/delete/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("message/", MessageList.as_view(), name="message_list"),
    path("message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
]
