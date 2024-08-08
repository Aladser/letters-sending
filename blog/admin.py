from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('header', 'content', 'published_at', 'views_count' , 'is_active')
    search_fields = ('header', 'content',)
    ordering = ('-published_at', 'header', 'content',)
