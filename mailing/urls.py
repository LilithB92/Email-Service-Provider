from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import RecipientList, RecipientDetailView, RecipientCreateView, RecipientUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path("recipient/", RecipientList.as_view(), name="recipient_list"),
    path("recipient_detail/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient/new/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
]
