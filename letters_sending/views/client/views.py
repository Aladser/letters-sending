from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from authen.services import CustomLoginRequiredMixin
from letters_sending.forms import ClientForm
from letters_sending.models import Client
from libs.custom_formatter import CustomFormatter


# СПИСОК
class ClientListView(CustomLoginRequiredMixin, ListView):
    model = Client
    template_name = "client/list.html"
    title = 'список клиентов'
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }


# СОЗДАТЬ
class ClientCreateView(CustomLoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "letters_sending.add_client"

    model = Client
    template_name = "form.html"
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    title = "добавить клиента"
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        context['back_url'] = reverse_lazy('client_list')

        return context


# ОБНОВИТЬ
class ClientUpdateView(CustomLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "letters_sending.change_client"

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


# УДАЛИТЬ
class ClientDeleteView(CustomLoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "letters_sending.delete_client"

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
