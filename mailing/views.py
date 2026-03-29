from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from mailing.models import Recipient


# Create your views here.
class RecipientList(ListView):
    model = Recipient
    context_object_name = "recipients"
