from django.contrib import admin
from .models import Asset, CommentRating
# Register your models here.

# Creating our slug pre-populate and the way the info is listed in admin.
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'user' , 'price', 'category', 'modified_date', 'is_available',)
    prepopulated_fields = {
        'slug': ('asset_name',)
    }

# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value', 'is_active',)
#     list_editable = ('is_active',)
#     list_filter = ('product', 'variation_category', 'variation_value',)

admin.site.register(Asset, AssetAdmin)
# admin.site.register(Variation, VariationAdmin)
admin.site.register(CommentRating)
