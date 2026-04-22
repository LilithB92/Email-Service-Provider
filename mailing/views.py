from django.contrib.auth.mixins import LoginRequiredMixin
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
from mailing.services import MailingAttemptService
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
    """
        Display recipients :model:`mailing.Recipient`.
        **Context**
        ``recipients``
            An instance of :model:`mailing.Recipient`.
        **Template:**
        :template:`mailing/recipient_list.html`
    """
    model = Recipient
    context_object_name = "recipients"
    paginate_by = 2

    def get_queryset(self):
        """Выбираем только рассылки Владелца."""
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """
      Display an individual recipient :model:`mailing.Recipient`.
      **Context**
      ``object``
          An instance of :model:`mailing.Recipient`.
      **Template:**
      :template:`mailing/recipient_list.html`
  """
    model = Recipient
    permission_required = "mailing.detail_recipient"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new Recipient instance.

    Attributes:
        model (Recipient): The model class that this view will create an instance of.
        form_class (RecipientForm): The custom ModelForm used for validation and display.
        template_name (str):`recipient_form` Path to the template used to render the form.
        success_url (str):`mailing:recipient_list` The URL to redirect to after a successful form submission.
    """
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        """
        Custom logic to execute when the form is valid.
        Args:
            form (RecipientForm): The validated form instance.
        Returns:
            HttpResponse: A redirect to the success_url.
        """
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """
       View to update a  Recipient instance.

      Attributes:
          model (Message): The model class that this view will create an instance of.
          form_class (RecipientForm): The custom ModelForm used for display.
          template_name (str):`recipient_form.html` Path to the template used to render the form.
          success_url (str):`mailing:recipient_list` The URL to redirect to after a successful form submission.
      """
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        """
       Custom logic to execute when the form is valid.
       Args:
           form (RecipientForm): The validated form instance.
       Returns:
           HttpResponse: A redirect to the success_url.
       """
        user = self.request.user
        recipient = form.save()
        if user == recipient.owner:
            recipient.save()
        elif user.groups.filter(name="Manager").exists():
            return HttpResponseForbidden("У вас нет прав редактирование рассылок.")
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
       View to delete a Recipient instance.

       Attributes:
           model(Recipient): The model this view operates on (Post).
           success_url:`mailing:recipient_list` The URL to redirect to after the object is deleted.
           template_name:`recipient_confirm_delete.html`.Custom template for confirming deletion.
       """

    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

    def test_func(self):
        """Allow  to delete only for superusers or specific criteria"""
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


class MessageList(LoginRequiredMixin, ListView):
    """
        Display  messages :model:`mailing.Message`.
        **Context**
        ``messages``
            An instance of :model:`mailing.Message`.
        **Template:**
        :template:`mailing/message_list.html`
    """
    model = Message
    context_object_name = "messages"
    paginate_by = 2

    def get_queryset(self):
        """Фильтруем queryset по владельцу (owner)"""
        user = self.request.user
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
       Display a message :model:`mailing.Message`.
       **Context**
       `object`
           An instance of :model:`mailing.Message`.
       **Template:**
       :template:`mailing/message_detail.html`
   """
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
   View to create a new message instance.

   Attributes:
       model (Message): The model class that this view will create an instance of.
       form_class (MessageForm): The custom ModelForm used for display.
       template_name (str):`message_form` Path to the template used to render the form.
       success_url (str):`mailing:message_list` The URL to redirect to after a successful form submission.
   """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        """
       Custom logic to execute when the form is valid.
       Args:
           form (MessageForm): The validated form instance.
       Returns:
           HttpResponse: A redirect to the success_url.
       """
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update a new Message instance.

   Attributes:
       model (Message): The model class that this view will create an instance of.
       form_class (MessageForm): The custom ModelForm used for display.
       template_name (str):`message_form` Path to the template used to render the form.
       success_url (str):`mailing:message_list` The URL to redirect to after a successful form submission.
   """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        """
      Custom logic to execute when the form is valid.
      Args:
          form (MessageForm): The validated form instance.
      Returns:
          HttpResponse: A redirect to the success_url.
      """
        user = self.request.user
        message = form.save()
        if user == message.owner:
            message.save()
        elif user.groups.filter(name="Manager").exists():
            return HttpResponseForbidden("У вас нет прав редактирование сообщение.")
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete a Message instance.

    Attributes:
        model(Message): The model this view operates on (Post).
        success_url:`mailing:message_list` The URL to redirect to after the object is deleted.
        template_name:`message_confirm_delete.html`.Custom template for confirming deletion.
    """
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def test_func(self):
        """ Allow delete only for superusers or specific criteria"""
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


class MailingList(LoginRequiredMixin, ListView):
    """
        Display Mailings :model:`mailing.Mailing`.
        **Context**
        ``mailings``
            An instance of :model:`mailing.Mailing`.
        **Template:**
        :template:`mailing/mailing_list.html`
    """
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
    """
        Display a Mailing :model:`mailing.Mailing`.
        **Context**
        `object`
            An instance of :model:`mailing.Mailing`.
        **Template:**
        :template:`mailing/mailing_detail.html`
    """

    def get_object(self, queryset=None):
        """Update status in the page"""
        obj = super().get_object(queryset)
        self.update_status(obj)
        return obj

    def update_status(self, object):
        """ Update mailing.Mailing models status"""
        current_time = timezone.now()
        if object.end_time <= current_time:
            object.status = "completed"
        elif object.start_time < current_time < object.end_time:
            object.status = "running"
        else:
            object.status = "created"
        object.save()


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
       View to create a new Mailing instance.

       Attributes:
           model (Mailing): The model class that this view will create an instance of.
           form_class (MailingForm): The custom ModelForm used for display.
           template_name (str):`mailing_form.html` Path to the template used to render the form.
           success_url (str):`mailing:mailing_list` The URL to redirect to after a successful form submission.
       """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        """
          Custom logic to execute when the form is valid.
          Args:
              form (RecipientForm): The validated form instance.
          Returns:
              HttpResponse: A redirect to the success_url.
        """
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
       View to update a new Mailing instance.

      Attributes:
          model (Mailing): The model class that this view will create an instance of.
          form_class (MailingForm): The custom ModelForm used for display.
          template_name (str):`mailing_form.html` Path to the template used to render the form.
          success_url (str):`mailing:mailing_list` The URL to redirect to after a successful form submission.
      """
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        """
          Custom logic to execute when the form is valid.
          Args:
              form (MailingForm): The validated form instance.
          Returns:
              HttpResponse: A redirect to the success_url.
          """
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
    """
        View to delete a Mailing instance.

        Attributes:
            model(Mailing): The model this view operates on (Post).
            success_url:`mailing:mailing_list` The URL to redirect to after the object is deleted.
            template_name:`mailing_confirm_delete.html`.Custom template for confirming deletion.
        """
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        """Not allow  managers to delete"""
        manager = self.request.user.groups.filter(name="Manager").exists()
        return not manager


class SendMailingDetailView(LoginRequiredMixin, DetailView):
    """
        Send a Mailing :model:`mailing.Mailing`.
        **Context**
        `object`
            An instance of :model:`mailing.Mailing`.
        **Template:**
        :template:`mailing/mailing_detail.html`
    """
    model = Mailing

    def get_object(self, queryset=None):
        """
        Send mail and create instance of Mailing_Attempt
        """
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
    """
        Display an individual :model:`mailing.MailingAttempt`.
        **Context**

        `mailing_attempts`
            An instance of :model:`mailing.MailingAttempt`.
        `attampt_mailing_count`
            An instance of :model:`mailing.MailingAttempt`, :service:` MailingAttemptService`.
        `success_attampt_mailing`
            An instance of :model:`mailing.MailingAttempt`, :service:` MailingAttemptService`.
        **Template:**
        :template:`mailing/mailingattempt_list.html`
    """
    model = MailingAttempt
    context_object_name = "mailing_attempts"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context["attampt_mailing_count"] = MailingAttemptService.get_mailing_attempts_count()
        context["success_attampt_mailing"] = MailingAttemptService.get_success_attempts_count()
        return context


class DisableMailing(LoginRequiredMixin, View):
    """
    Allow managers to disable mailing
    """
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if not request.user.has_perm("mailing.can_disable_mailing"):
            return HttpResponseForbidden("У вас нет прав для Отключение рассылок.")
        mailing.is_active = False
        mailing.save()
        return redirect(reverse("mailing:mailing_list"))
