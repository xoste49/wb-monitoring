from django.contrib import admin

from .models import Articles, ProductHistory, Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article')
    search_fields = ('user',)
    list_filter = ('id', 'user', 'article')
    empty_value_display = '-пусто-'


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    exclude = ('',)


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ('article', 'brand', 'name', 'seller', 'final_price', 'old_price', 'add_date')
    ordering = ['-add_date']
