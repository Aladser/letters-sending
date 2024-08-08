from django.views.generic import ListView, DetailView

from authen.services import CustomLoginRequiredMixin
from blog.models import Blog

TEMPLATE_FOLDER = "blog/"


# СПИСОК БЛОГОВ
class BlogListView(CustomLoginRequiredMixin, ListView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "list.html"

    def get_queryset(self):
        return super().get_queryset().order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['header'] = "Блоги"

        return context


# ДЕТАЛИ БЛОГА
class BlogDetailView(CustomLoginRequiredMixin, DetailView):
    model = Blog
    template_name = TEMPLATE_FOLDER + "detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"Блог №{self.object.header}"
        context['title'] = context['header'] = title

        return context
