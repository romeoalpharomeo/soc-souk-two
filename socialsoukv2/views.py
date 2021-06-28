from django.shortcuts import render, get_object_or_404
from store.models import Asset
from category.models import Category
from favorites.views import _favorites_id
from favorites.models import Favorites, FavoritesItem


def home(request):

    assets = Asset.objects.all().filter(is_available=True)

    context = {
        'assets': assets,
        # 'in_favorites': in_favorites,

    }
    return render(request, 'home.html', context)

