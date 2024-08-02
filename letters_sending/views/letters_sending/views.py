from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from letters_sending.forms import LettersSendingCreateForm, LettersSendingUpdateForm
from letters_sending.models import LettersSending
from libs import send_letters, CustomFormatter, CustomLoginRequiredMixin

TEMPLATE_FOLDER = "letters_sending/"


class LettersSendingListView(ListView):
    """LIST"""
    model = LettersSending
    template_name = TEMPLATE_FOLDER + "list.html"
    extra_context = {
        'title': '',
        'header': "cписок рассылок",
        'css_list': ("letters_sending.css",)
    }


class LettersSendingDetailView(DetailView):
    """DETAIL"""
    model = LettersSending
    template_name = TEMPLATE_FOLDER + "detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"рассылка №{self.object.pk}"
        context['title'] = context['header'] = title

        return context


class LettersSendingCreateView(CustomLoginRequiredMixin, CreateView):
    """CREATE"""

    model = LettersSending
    template_name = "form.html"
    form_class = LettersSendingCreateForm
    title = "добавить рассылку"
    extra_context = {
        'title': title,
        'header': title
    }

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            # установка даты первой отправки сообщений
            if self.object.status.name == "launched" and not self.object.first_sending:
                self.object.first_sending = datetime.now()
            self.object.next_sending = self.object.first_sending
            self.object.save()

            if self.object.status.name == "launched":
                # запуск задачи
                send_letters(self.object)
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy('letter_sending_list')

        return context

    def get_success_url(self):
        return reverse_lazy("letter_sending_detail", kwargs={"pk": self.object.pk})


class LettersSendingUpdateView(CustomLoginRequiredMixin, UpdateView):
    """UPDATE"""

    model = LettersSending
    template_name = "form.html"
    form_class = LettersSendingUpdateForm

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            if self.object.status.name == "launched":
                if not self.object.first_sending:
                    self.object.first_sending = datetime.now()
                if not self.object.next_sending:
                    self.object.next_sending = self.object.first_sending
                if self.object.next_sending <= datetime.now():
                    # если время запуска просрочено
                    send_letters(self.object)
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("letter_sending_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"изменить рассылку №{self.object.pk}"
        context['title'] = context['header'] = title
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy("letter_sending_detail", kwargs={"pk": self.object.pk})

        return context


class LettersSendingDeleteView(CustomLoginRequiredMixin, DeleteView):
    """DELETE"""

    model = LettersSending
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('letter_sending_list')
    extra_context = {
        'css_list': ("confirm_delete.css",),
        "type": "рассылку",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = f"удаление рассылки №{self.object.pk}"
        context['object_type_name'] = "рассылку"
        context['back_url'] = reverse_lazy("letter_sending_detail", kwargs={"pk": self.object.pk})

        return context
