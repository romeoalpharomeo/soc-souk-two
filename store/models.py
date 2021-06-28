from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account, UserProfile
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify

# Create your models here.

class Asset(models.Model):
    asset_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=2)
    images = models.ImageField(upload_to='photos/assets')
    is_available = models.BooleanField(default=True)

    # If we delete a category, then all of the products associated with that category will be deleted as well.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     #this line below give to the instance slug field a slug name
    #     self.slug = slugify(self.asset_name)
    #     #this line below save every fields of the model instance
    #     super(Asset, self).save(*args, **kwargs) 

    def average_rating(self):
        comments = CommentRating.objects.filter(asset=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if comments['average'] is not None:
            avg = float(comments['average'])
        return avg

    def count_comment(self):
        comments = CommentRating.objects.filter(asset=self, status=True).aggregate(count=Count('id'))
        count = 0
        if comments['count'] is not None:
            count = int(comments['count'])
        return count
        



    def get_url(self):
        # The args that are passed for this, self refers to Asset model, category refers to the category model and slug refers to the slug of the category model. Then, the self (Asset) slug is passed in. These two slugs combined will give us the url pattern that we defined for the asset detail page, which you can find in the urls file of this app.
        return reverse('asset_detail', args=[self.category.slug, self.slug])

    # Creates a string representation set to the product name.
    def __str__(self):
        return self.asset_name

# With the addition of this class, we can now choose between which set() we want to get when displaying our variations, ie, set.colors OR set.sizes
# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category = 'color', is_active=True)

#     def sizes(self):
#         return super(VariationManager, self).filter(variation_category = 'size', is_active=True)


# Here, we make our potential variation category choices into a tuple
# variation_category_choices = (
#     ('color', 'color'),
#     ('size', 'size'),
# )
# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # Here, we set the choices equal to our pre-declared variable of category choices
#     variation_category = models.CharField(max_length=100, choices=variation_category_choices)
#     variation_value = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now=True)

#     # This connects our variation manager class to our variation model here
#     objects = VariationManager()

#     def __str__(self):
#         return self.variation_value

class CommentRating(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
