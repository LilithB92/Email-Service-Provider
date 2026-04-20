from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from mailing.forms import MailingForm
from mailing.forms import MessageForm
from mailing.forms import RecipientForm
from mailing.models import Mailing
from mailing.models import Message
from mailing.models import Recipient
from mailing.services import MailingRecipientService
from mailing.services import SendMailing


class HomePageView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_mailings"] = MailingRecipientService.count_mailings()
        context["count_recipients"] = MailingRecipientService.count_recipients()
        context["active_mailings_count"] = MailingRecipientService.active_mailings_count()
        return context


class RecipientList(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = "recipients"
    paginate_by = 3


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"
    paginate_by = 2


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MailingList(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"
    paginate = 2


class MailingDetailView(LoginRequiredMixin, DetailView):
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


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


class SendMailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        # 1. Get the object normally
        obj = super().get_object(queryset)
        pk = obj.pk
        send_mailing = SendMailing()
        recipients = obj.recipients.all()
        try:
            for recipient in recipients:
                SendMailing.send_mailing(send_mailing, pk=pk, recipient=recipient)
                SendMailing.save_mailing_attempt(send_mailing, pk=pk, status="success")
        except Exception as e:
            SendMailing.save_mailing_attempt(send_mailing, pk=pk, ex=e)
        return obj
