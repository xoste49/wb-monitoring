from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Articles

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'favorites']
    # list_display = ('name', 'email')
    ordering = ['username']
    search_fields = ['username']


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    exclude = ('',)
