from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from mailing.forms import MailingForm
from mailing.forms import MessageForm
from mailing.forms import RecipientForm
from mailing.models import Mailing
from mailing.models import Message
from mailing.models import Recipient


# Create your views here.
class RecipientList(ListView):
    """"""

    model = Recipient
    context_object_name = "recipients"
    paginate_by = 3


class RecipientDetailView(DetailView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")


class MessageList(ListView):
    model = Message
    context_object_name = "messages"
    paginate_by = 2


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MailingList(ListView):
    model = Mailing
    context_object_name = "mailings"
    paginate = 2


class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.update_status(obj)
        return obj

    def update_status(self, object):
        current_time = timezone.now()
        if object.end_time <= current_time:
            object.status = "completed"
        elif object.start_time < current_time < object.end_time:
            object.status = "running"
        else:
            object.status = "created"
        object.save()


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})
