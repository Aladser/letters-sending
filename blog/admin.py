from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('header', 'content', 'views_count', 'published_at')
    search_fields = ('header', 'content',)
    ordering = ('header', 'content',)
