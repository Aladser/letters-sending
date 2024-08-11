from django.views.generic import ListView, DetailView

from blog.models import Blog
from libs.managed_cache_mixin import ManagedCacheMixin

TEMPLATE_FOLDER = "blog/"
CACHED_DETAIL_BLOG_KEY = 'detail_letterssending_'
"""ключ хранилища ключей кэшей детальных страниц блогов"""

# СПИСОК БЛОГОВ
class BlogListView(ManagedCacheMixin, ListView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "list.html"
    cached_key = 'view_blog'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = "Блоги"

        return context


# ДЕТАЛИ БЛОГА
class BlogDetailView(ManagedCacheMixin, DetailView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "detail.html"
    cached_key = CACHED_DETAIL_BLOG_KEY

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"Блог №{self.object.pk}"
        context['title'] = context['header'] = title

        return context
