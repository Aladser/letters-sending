from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from letters_sending.forms import MessageForm
from letters_sending.models import Message
from libs.custom_formatter import CustomFormatter
from libs.login_required_mixin import CustomLoginRequiredMixin

TEMPLATE_FOLDER = "message/"


class MessageListView(ListView):
    """LIST"""
    model = Message
    template_name = TEMPLATE_FOLDER + "list.html"
    title = 'список сообщений'
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }


class MessageDetailView(DetailView):
    """DETAIL"""
    model = Message
    template_name = TEMPLATE_FOLDER + "detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"cообщение №{self.object.pk}"
        context['title'] = title
        context['header'] = title.capitalize()
        context['object'].content = context['object'].content.replace('\n', '<br>')

        return context


class MessageCreateView(CustomLoginRequiredMixin, CreateView):
    """CREATE"""

    model = Message
    template_name = "form.html"
    form_class = MessageForm
    title = f"создать сообщение"
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy('message_list')

        return context

    def get_success_url(self):
        return reverse_lazy("message_detail", kwargs={"pk": self.object.pk})


class MessageUpdateView(CustomLoginRequiredMixin, UpdateView):
    """UPDATE"""

    model = Message
    template_name = "form.html"
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy("message_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"Изменить сообщение {self.object.pk}"
        context['title'] = title
        context['header'] = title.capitalize()
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy("message_detail", kwargs={"pk": self.object.pk})

        return context


class MessageDeleteView(CustomLoginRequiredMixin, DeleteView):
    """DELETE"""

    model = Message
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('message_list')
    extra_context = {'css_list': ("confirm_delete.css",)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title = f"удаление сообщения {self.object.pk}"
        context['title'] = title
        context['header'] = title.capitalize()

        context['object_type_name'] = "сообщение"
        if self.request.GET['type'] == 'list':
            context['back_url'] = reverse_lazy("message_list")
        else:
            context['back_url'] = reverse_lazy("message_detail", kwargs={"pk": self.object.pk})

        return context

