from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorites, name='favorites'),
    path('add_favorites/<int:asset_id>/', views.add_favorites, name='add_favorites'),
    path('remove_favorites/<int:asset_id>/<int:favorites_item_id>/', views.remove_favorites, name='remove_favorites'),
]

