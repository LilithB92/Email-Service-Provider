from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from mailing.forms import RecipientForm
from mailing.models import Recipient


# Create your views here.
class RecipientList(ListView):
    model = Recipient
    context_object_name = 'recipients'
    paginate_by = 3


class RecipientDetailView(DetailView):
    model = Recipient
#
#
# class RecipientCreateView(CreateView):
#     model = Recipient
#     success_url = reverse_lazy("mailing:recipients_list")
#
#
# class RecipientUpdateView(UpdateView):
#     model = Recipient
#     form_class = RecipientForm
#     success_url = reverse_lazy("mailing:recipients_list")
#
#
#
# class RecipientDeleteView(DeleteView):
#     model = Recipient
#     success_url = reverse_lazy("mailing:recipients_list")
