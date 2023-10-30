from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name',)
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)
    empty_value_display = '-empty-'
