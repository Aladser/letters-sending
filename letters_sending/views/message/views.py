from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from authen.services import CustomLoginRequiredMixin
from letters_sending.apps import LetterConfig
from letters_sending.forms import MessageForm
from letters_sending.models import Message
from letters_sending.services.services import OwnerListVerificationMixin
from libs.managed_cache import ManagedCache
from libs.managed_cache_mixin import ManagedCachedMixin
from libs.custom_formatter import CustomFormatter

TEMPLATE_FOLDER = "message/"
CACHED_MESSAGES_KEY = 'view_message'
"""ключ хранилища ключей кэшей страницы списка сообщений"""

# СПИСОК СООБЩЕНИЙ
class MessageListView(CustomLoginRequiredMixin, OwnerListVerificationMixin, PermissionRequiredMixin,
                      ManagedCachedMixin, ListView):
    app_name = LetterConfig.name
    permission_required = app_name + ".view_owner_message"
    list_permission = app_name + '.view_message'
    list_owner_permission = app_name + '.view_owner_message'

    model = Message
    template_name = TEMPLATE_FOLDER + "list.html"
    title = 'Cписок сообщений'
    extra_context = {
        'title': title,
        'header': title
    }
    cached_key = CACHED_MESSAGES_KEY


# ДЕТАЛИ СООБЩЕНИЯ
class MessageDetailView(CustomLoginRequiredMixin, DetailView):
    model = Message
    template_name = TEMPLATE_FOLDER + "detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"cообщение №{self.object.pk}"
        context['title'] = title
        context['header'] = title.capitalize()
        context['object'].content = context['object'].content.replace('\n', '<br>')

        return context


# СОЗДАТЬ СООБЩЕНИЕ
class MessageCreateView(CustomLoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "letters_sending.add_message"

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

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

            ManagedCache.clear_data(CACHED_MESSAGES_KEY)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("message_detail", kwargs={"pk": self.object.pk})


# ОБНОВИТЬ СООБЩЕНИЕ
class MessageUpdateView(CustomLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "letters_sending.change_message"

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

        ManagedCache.clear_data(CACHED_MESSAGES_KEY)

        return context


# УДАЛИТЬ СООБЩЕНИЕ
class MessageDeleteView(CustomLoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "letters_sending.delete_message"

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

        ManagedCache.clear_data(CACHED_MESSAGES_KEY)

        return context
