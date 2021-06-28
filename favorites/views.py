from django.shortcuts import render, redirect, get_object_or_404
from store.models import Asset
from .models import Favorites, FavoritesItem

# Create your views here.

# Gets/creates session so we can create favorites based on session
def _favorites_id(request):
    favorites = request.session.session_key
    if not favorites:
        favorites = request.session.create()
    return favorites

def favorites(request, favorites_items=None):

    try:
        if request.user.is_authenticated:
            favorites_items = FavoritesItem.objects.filter(user=request.user, is_active=True)

        else:
            favorites = Favorites.objects.get(favorites_id=_favorites_id(request))
            favorites_items = FavoritesItem.objects.filter(favorites=favorites, is_active=True)

    except:
        pass

    context = {
        'favorites_items': favorites_items
    }
    return render(request, 'favorites/favorites.html', context)

def add_favorites(request, asset_id):
    current_user = request.user
    asset = Asset.objects.get(id=asset_id)

    if current_user.is_authenticated:
        favorites_item_exists = FavoritesItem.objects.filter(asset=asset, user=current_user).exists()
        if favorites_item_exists:
            favorites_item = FavoritesItem.objects.filter(asset=asset, user=current_user)
        else:
            favorites_item = FavoritesItem.objects.create(
                asset = asset,
                user = current_user,
            )
            favorites_item.save()
        return redirect('favorites')
    else:   
        try:
            favorites = Favorites.objects.get(favorites_id=_favorites_id(request))
        except Favorites.DoesNotExist:
            favorites = Favorites.objects.create(
            favorites_id=_favorites_id(request)
        )
        favorites.save()
    try:
        favorites_item = FavoritesItem.objects.get(asset=asset, favorites=favorites)
        favorites_item.save()
    except FavoritesItem.DoesNotExist:
        favorites_item = FavoritesItem.objects.create(
            asset = asset,
            favorites = favorites,
        )
        favorites_item.save()

    return redirect('favorites')

def remove_favorites(request, asset_id, favorites_item_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.user.is_authenticated:
        favorites_item = FavoritesItem.objects.get(asset=asset, user=request.user, id=favorites_item_id)
    else:
        
        favorites = Favorites.objects.get(favorites_id=_favorites_id(request))
        favorites_item = FavoritesItem.objects.get(asset=asset, favorites=favorites)
        
    favorites_item.delete()
    return redirect('favorites')
