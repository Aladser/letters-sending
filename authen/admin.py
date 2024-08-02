from django.contrib import admin
from authen.models import Country, User


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'is_active')
    search_fields = ('first_name', 'last_name')
