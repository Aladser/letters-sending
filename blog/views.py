from django.views.generic import ListView, DetailView
from blog.models import Blog
from libs.managed_cache_mixin import ManagedCacheMixin

TEMPLATE_FOLDER = "blog/"
CACHED_LIST_BLOG_KEY = 'view_blog'
"""ключ хранилища ключей кэшей списка блогов"""


# СПИСОК БЛОГОВ
class BlogListView(ManagedCacheMixin, ListView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "list.html"
    cached_key = CACHED_LIST_BLOG_KEY
    extra_context = {
        'title': "Блоги",
        'header': "Блоги"
    }

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-published_at')


# ДЕТАЛИ БЛОГА
class BlogDetailView(DetailView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "detail.html"

    def get_object(self, queryset=None):
        # увеличение счетчика просмотров
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = f"Блог {self.object.pk}"

        return context
