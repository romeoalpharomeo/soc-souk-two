from django.contrib import admin
from .models import Favorites, FavoritesItem
# Register your models here.

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('favorites_id', 'date_added')

class FavoritesItemAdmin(admin.ModelAdmin):
    list_display = ('asset', 'favorites', 'is_active', 'user')

admin.site.register(Favorites, FavoritesAdmin)

admin.site.register(FavoritesItem, FavoritesItemAdmin)