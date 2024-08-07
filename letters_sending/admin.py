from django.contrib import admin
from letters_sending.models import Message, Client, DatePeriod, Status, LettersSending, Attempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'owner')
    search_fields = ('subject',)
    ordering = ("pk",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'surname', 'name', 'patronym', "comment", 'owner')
    search_fields = ('email', 'surname', 'name', 'patronym')
    ordering = ("email",)


@admin.register(DatePeriod)
class DatePeriodAdmin(admin.ModelAdmin):
    list_display = ('name', "description", "interval")
    ordering = ("pk",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', "description")
    ordering = ("pk",)


@admin.register(LettersSending)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('message', "period", 'status', 'first_sending', 'next_sending', 'owner')
    ordering = ("next_sending", "status", "period")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('letters_sending', "recipient", "response", 'is_sent', "created_at")
    ordering = ("created_at", "is_sent")
