from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField

from .models import Recipient



class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ["email"]


    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.help_text


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if '@' not in email:
            raise ValidationError("email не корректно")
        return email

