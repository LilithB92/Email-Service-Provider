from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomePageView, DisableMailing
from mailing.views import MailingAttemptList
from mailing.views import MailingCreateView
from mailing.views import MailingDeleteView
from mailing.views import MailingDetailView
from mailing.views import MailingList
from mailing.views import MailingUpdateView
from mailing.views import MessageCreateView
from mailing.views import MessageDeleteView
from mailing.views import MessageDetailView
from mailing.views import MessageList
from mailing.views import MessageUpdateView
from mailing.views import RecipientCreateView
from mailing.views import RecipientDeleteView
from mailing.views import RecipientDetailView
from mailing.views import RecipientList
from mailing.views import RecipientUpdateView
from mailing.views import SendMailingDetailView

app_name = MailingConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
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
    path("'mailing/", MailingList.as_view(), name="mailing_list"),
    path("mailing_detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("send_mailig/<int:pk>/", SendMailingDetailView.as_view(), name="send_mailing"),
    path("mailing_attempt/", MailingAttemptList.as_view(), name="mailing_attempt_list"),
    path("disable_mailing/<int:pk>/", DisableMailing.as_view(), name="disable_mailing"),
]
