from django.db import models
from store.models import Asset
from accounts.models import Account

# Create your models here.

class Favorites(models.Model):
    favorites_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.favorites_id


class FavoritesItem(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)


    def __unicode__(self):
        return self.asset