from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from authen.services import CustomLoginRequiredMixin
from letters_sending.forms import ClientForm
from letters_sending.models import Client
from letters_sending.services.services import OwnerVerificationMixin
from libs.custom_formatter import CustomFormatter


# СПИСОК КЛИЕНТОВ
class ClientListView(CustomLoginRequiredMixin, ListView):
    model = Client
    template_name = "client/list.html"
    title = 'Cписок клиентов'
    extra_context = {
        'title': title,
        'header': title
    }

    def get_queryset(self):
        if self.request.user.has_perm('letters_sending.view_client'):
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)

# СОЗДАТЬ КЛИЕНТА
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


# ОБНОВИТЬ КЛИЕНТА
class ClientUpdateView(CustomLoginRequiredMixin, PermissionRequiredMixin, OwnerVerificationMixin, UpdateView):
    permission_required = "letters_sending.change_client"

    model = Client
    template_name = "form.html"
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    title = 'Изменить клиента'
    extra_context = {
        'title': title,
        'header': title,
        'back_url': success_url
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["required_fields"] = CustomFormatter.get_form_required_field_labels(context["form"])
        return context


# УДАЛИТЬ  КЛИЕНТА
class ClientDeleteView(CustomLoginRequiredMixin, PermissionRequiredMixin, OwnerVerificationMixin, DeleteView):
    permission_required = "letters_sending.delete_client"

    model = Client
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('client_list')

    title = "удаление клиента"
    extra_context = {
        'css_list': ("confirm_delete.css",),
        'title': title,
        'header': title,
        'back_url': success_url,
        'object_type_name': "клиента"
    }

