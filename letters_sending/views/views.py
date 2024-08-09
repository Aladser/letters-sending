from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from authen.services import CustomLoginRequiredMixin
from blog.models import Blog
from config.settings import APP_NAME
from letters_sending.models import Attempt, LettersSending, Status, Client
import random

# СПИСОК ПОПЫТОК
class AttemptListView(CustomLoginRequiredMixin, ListView):
    model = Attempt
    template_name = "attempt_list.html"

    title = "Статистика рассылок"
    extra_context = {
        'title': title,
        'header': title,
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.order_by('letters_sending').values('letters_sending', 'response').annotate(count=Count('id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for attempt in context['object_list']:
            sending = LettersSending.objects.get(pk=attempt['letters_sending'])
            attempt['message'] = sending.message
            attempt['status'] = sending.status

        return context


# ГЛАВНАЯ СТРАНИЦА
def index_page(request):
    blog_list = Blog.objects.all()
    blog_list_count = blog_list.count()
    if blog_list_count > 3:
        # случайные индексы
        blog_indexes_list = [i for i in range(blog_list_count)]
        random.shuffle(blog_indexes_list)

        blog_list = [blog_list[blog_indexes_list[i]] for i in range(3)]

    print(blog_list)
    context = {
        'header':APP_NAME,
        'sendings_count': LettersSending.objects.all().count(),
        'active_sendings_count': LettersSending.objects.filter(status= Status.objects.get(name='launched')).count(),
        'clients_count': Client.objects.all().count(),
        'blog_list': blog_list,
    }

    return render(request, 'index.html', context)
