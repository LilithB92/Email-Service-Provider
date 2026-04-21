from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
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
from mailing.models import MailingAttempt
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
    paginate_by = 2

    def get_queryset(self):
        """Выбираем только рассылки Владелца."""
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=user)


class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recipient
    permission_required = "mailing.delete_recipient"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        user = self.request.user
        recipient = form.save()
        if user == recipient.owner:
            recipient.save()
        elif user.groups.filter(name="Manager").exists():
            return HttpResponseForbidden("У вас нет прав редактирование рассылок.")
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

    def test_func(self):
        # Allow delete only for superusers or specific criteria
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"
    paginate_by = 2

    def get_queryset(self):
        """Фильтруем queryset по владельцу (owner)"""
        user = self.request.user
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        user = self.request.user
        message = form.save()
        if user == message.owner:
            message.save()
        elif user.groups.filter(name="Manager").exists():
            return HttpResponseForbidden("У вас нет прав редактирование сообщение.")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def test_func(self):
        # Allow delete only for superusers or specific criteria
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


class MailingList(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"
    paginate_by = 2

    def get_queryset(self):
        """Фильтруем queryset по владельцу (owner)"""
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Mailing.objects.filter(is_active=True)
        return Mailing.objects.filter(owner=user, is_active=True)


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

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        user = self.request.user
        mailing = form.save()
        if user == mailing.owner:
            mailing.save()
        elif user.groups.filter(name="Manager").exists():
            return HttpResponseForbidden("У вас нет прав редактирование рассылок.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        # Not allow delete managers
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


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


class MailingAttemptList(LoginRequiredMixin, ListView):
    model = MailingAttempt
    context_object_name = "mailing_attempts"
    paginate_by = 2


class DisableMailing(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if not request.user.has_perm("mailing.can_disable_mailing"):
            return HttpResponseForbidden("У вас нет прав для Отключение рассылок.")
        mailing.is_active = False
        mailing.save()
        return redirect(reverse("mailing:mailing_list"))
