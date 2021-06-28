from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, CommentRating
from accounts.models import UserProfile
from category.models import Category
from favorites.views import _favorites_id
from favorites.models import Favorites, FavoritesItem
from django.db.models import Q
from .forms import CommentForm, AssetForm
from django.contrib import messages


# Create your views here.

def store(request, category_slug=None):
    categories = None
    assets_with_price = None

    # Sets up the condition if their is a category slug present in request
    if category_slug is not None:
        # Gets the slug if it exists or returns 404 error
        categories = get_object_or_404(Category, slug=category_slug)
        # Gets all assets associated with that category AND excludes the assets where price is equal to 0
        assets_with_price = Asset.objects.filter(category=categories, is_available=True).exclude(price=0)
        # Counts the assets in the given queryset
        asset_count = assets_with_price.count()
    else:
        # This line will only pull assets with a price that does not equal 0
        assets_with_price = Asset.objects.exclude(price=0)
        # Gets the total amount of assets 
        asset_count = assets_with_price.count()

    context = {
        'assets_with_price': assets_with_price,
        'asset_count': asset_count,
    }
    return render(request, 'store/store.html', context)

def asset_detail(request, category_slug, asset_slug ):
    try:
        # Here, we are getting the slugs for the category and the product. First, we access the category slug by using the double underscore, this is the syntax to get the slug attribute from that model, then we set it equal to the category slug. 
        single_asset = Asset.objects.get(category__slug=category_slug, slug=asset_slug)
        # Here, we are checking cart items by accessing the cart model followed by double underscore and then the attribute cart id in the Cart model then we are checking the single product (whatever product the user is currently viewing in product detail view). Finally, we add the .exists function so that it returns True or False

        in_favorites = FavoritesItem.objects.filter(favorites__favorites_id=_favorites_id(request), asset=single_asset).exists()

        # return HttpResponse(in_cart) This is GREAT for testing and troubleshooting code
        # exit()
    except Exception as e:
        raise e
    
    
    comments = CommentRating.objects.filter(asset_id=single_asset.id, status=True)
    
    
    context = {
        'single_asset': single_asset,
        'in_favorites': in_favorites,
        'comments': comments,
    }

    return render(request, 'store/asset_detail.html', context)

def search(request):
    # We set the name of our form input to keyword, so the first thing we do is check to see if the get rquest has the keyword
    if 'keyword' in request.GET:
        # Here, we are setting the keywords value to whatever is entered and submitted
        keyword = request.GET['keyword']
        # This next line will handle if a keyword is present/exists
        if keyword:
            # __icontains will look for match within description of whatever the keyword value is in this case, Q() lets us bring in multiple query sets and use OR operators
            assets_with_price = Asset.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(asset_name__icontains=keyword) | Q(category__category_name__icontains=keyword)).exclude(price=0)
            asset_count = assets_with_price.count()
    context = {
        'assets_with_price': assets_with_price,
        'asset_count' : asset_count,
    }
    return render(request, 'store/store.html', context)

def submit_comment(request, asset_id):
    # STORE THE CURRENT PAGE URL
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # try:
        #     # The double underscore is pointing to the user and product field in the ReviewRating class
        #     comments = CommentRating.objects.get(user__id=request.user.id, asset__id=asset_id)
        #     # Passing in instance will update a review if the user posting has already made one, this is not ideal for comment posting but may be useful if you want to limit spamming of review section
        #     form = CommentForm(request.POST, instance=comments)
        #     form.save()
        #     messages.success(request, 'Thank you! Your comment has been updated.')
        #     return redirect(url)

        # except CommentRating.DoesNotExist:
        form = CommentForm(request.POST)
        if form.is_valid():
            data = CommentRating()
            data.rating = form.cleaned_data['rating']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.asset_id = asset_id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thanks! Your comment was submitted.')
            return redirect(url)





