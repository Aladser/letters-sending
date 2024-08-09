from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from authen.services import CustomLoginRequiredMixin
from blog.models import Blog
from config.settings import APP_NAME, CACHED_ENABLED
from letters_sending.apps import LetterConfig
from letters_sending.models import Attempt, LettersSending, Status, Client
import random

from letters_sending.services.services import OwnerListVerificationMixin


# СПИСОК ПОПЫТОК
class AttemptListView(CustomLoginRequiredMixin, PermissionRequiredMixin, ListView):
    app_name = LetterConfig.name
    permission_required = app_name + ".view_owner_stat_letterssending"
    list_permission = app_name + '.view_stat_letterssending'
    list_owner_permission = app_name + '.view_owner_stat_letterssending'

    model = Attempt
    template_name = "attempt_list.html"

    title = "Статистика рассылок"
    extra_context = {
        'title': title,
        'header': title,
    }

    def get_queryset(self, *args, **kwargs):
        if self.request.user.has_perm(self.list_owner_permission):
            # все заявки
            queryset = super().get_queryset(*args, **kwargs)
            queryset = queryset.order_by('letters_sending').values('letters_sending', 'response').annotate(count=Count('id'))

            if not self.request.user.has_perm(self.list_permission):
                # только свои заявки
                object_list = []
                for set in queryset:
                    if LettersSending.objects.get(pk=set['letters_sending']).owner == self.request.user:
                        object_list.append(set)
                return object_list

            return queryset
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for attempt in context['object_list']:
            sending = LettersSending.objects.get(pk=attempt['letters_sending'])
            attempt['message'] = sending.message
            attempt['status'] = sending.status
            attempt['owner'] = sending.owner


        return context


# ГЛАВНАЯ СТРАНИЦА
def index_page(request):
    cached_key = f'index_{request.user.pk}'
    if CACHED_ENABLED:
        cached_data = cache.get(cached_key)
        if cached_data is not None:
            return cached_data


    blog_list = Blog.objects.all()
    blog_list_count = blog_list.count()
    if blog_list_count > 3:
        # случайные индексы
        blog_indexes_list = [i for i in range(blog_list_count)]
        random.shuffle(blog_indexes_list)

        blog_list = [blog_list[blog_indexes_list[i]] for i in range(3)]

    context = {
        'header':APP_NAME,
        'sendings_count': LettersSending.objects.all().count(),
        'active_sendings_count': LettersSending.objects.filter(status= Status.objects.get(name='launched')).count(),
        'clients_count': Client.objects.all().count(),
        'blog_list': blog_list,
    }

    response = render(request, 'index.html', context)
    if CACHED_ENABLED:
        cache.set(cached_key, response)
    return response
