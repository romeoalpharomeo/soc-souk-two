from django.contrib import admin
from .models import Category

# Register your models here.

# We are creating this so that we can add pre-population of the slug field in our category model.
class CategoryAdmin(admin.ModelAdmin):
    # Now, when we start to type in our category name, the slug field will populate at the same time.
    prepopulated_fields = {
        'slug': ('category_name',)
    }
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)
