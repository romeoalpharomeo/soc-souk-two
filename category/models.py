from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # We are creating a function in order to return the slug as the url for the category. When we create a function within our class, we need to pass in self
    def get_url(self):
        # Here, we are bringing in the path that we created for our categories in the store urls file as well as passing an argument that refers to the slug attribute in this model
        return reverse('assets_by_category_store', args=[self.slug])

    
    # When we return the Category object inside our template this should return the category name.
    def __str__(self):
        return self.category_name