import datetime

from django.forms import ModelForm, BooleanField, DateInput, DateTimeInput
from django import forms

from config.settings import DATETIME_FORMAT
from letters_sending.models import LettersSending, Message, Client


class GeneralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # стилизация полей
        for field in self.fields.values():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control mb-2'
            else:
                field.widget.attrs['class'] = 'mb-2'


class LettersSendingCreateForm(GeneralForm):
    now_date = datetime.date.today()
    first_sending = forms.DateTimeField(
        label="Дата первой отправки",
        required=False,
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        localize=True
    )

    class Meta:
        model = LettersSending
        fields = ('message', 'clients', 'first_sending', 'period', 'status')


class LettersSendingUpdateForm(GeneralForm):
    next_sending = forms.DateTimeField(
        label="Дата следующей отправки",
        required=False,
        widget=DateTimeInput(format=DATETIME_FORMAT, attrs={'type': 'datetime-local'}),
        localize=True
    )

    class Meta:
        model = LettersSending
        fields = ('message', 'clients', 'next_sending', 'period', 'status', 'is_active')


class MessageForm(GeneralForm):
    class Meta:
        model = Message
        fields = ('subject', 'content')


class ClientForm(GeneralForm):
    comment = forms.CharField(widget=forms.Textarea, label="Заметка", required=False)

    class Meta:
        model = Client
        fields = ('email', 'surname', 'name', 'patronym', 'comment')

