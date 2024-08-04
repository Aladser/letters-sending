from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from letters_sending.forms import ClientForm
from letters_sending.models import Client
from libs.custom_formatter import CustomFormatter
from libs.login_required_mixin import CustomLoginRequiredMixin


class ClientListView(ListView):
    """LIST"""

    model = Client
    template_name = "client/list.html"
    title = 'список клиентов'
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }


class ClientCreateView(CustomLoginRequiredMixin, CreateView):
    """CREATE"""

    model = Client
    template_name = "form.html"
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    title = "добавить клиента"
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy('client_list')

        return context


class ClientUpdateView(CustomLoginRequiredMixin, UpdateView):
    """UPDATE"""

    model = Client
    template_name = "form.html"
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        title = f"изменить клиента {self.object.email}"
        context['title'] = title
        context['header'] = title.capitalize()

        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy('client_list')

        return context


class ClientDeleteView(CustomLoginRequiredMixin, DeleteView):
    """DELETE"""

    model = Client
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('client_list')

    title = "удаление клиента"
    extra_context = {
        'css_list': ("confirm_delete.css",),
        'title': title,
        'header': title
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type_name'] = "клиента"
        context['back_url'] = self.success_url

        return context
