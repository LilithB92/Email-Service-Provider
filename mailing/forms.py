from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField

from .models import Mailing
from .models import Message
from .models import Recipient


class RecipientForm(forms.ModelForm):
    """
    Форма для отправки о получателе запросов
    """
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "post"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.help_text

    def clean_email(self):
        """
        Проверка для поля электронной почты. Гарантирует, что email имеет "@"
        """
        email = self.cleaned_data.get("email")
        if "@" not in email:
            raise ValidationError("email не корректно")
        return email


class MessageForm(forms.ModelForm):
    """Форма для отправки о сообщения запросов"""
    class Meta:
        model = Message
        fields = ["subject", "text"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingForm(forms.ModelForm):
    """Форма для отправки о рассылки запросов"""
    class Meta:
        model = Mailing
        fields = ("start_time", "end_time", "message", "recipients")
        widgets = {
            # Виджет 'date' вызывает календарь браузера
            "start_time": forms.DateInput(attrs={"type": "date"}),
            "end_time": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        """
        Проверка для даты и время начала отправки даты и времени окончания отправки. Гарантирует,
         что дата и время начала отправки не после даты и времени окончания отправки.
        """
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time >= end_time:
            raise forms.ValidationError(
                "Дата и время начала отправки не может быть после даты и времени окончания отправки"
            )
        return cleaned_data
