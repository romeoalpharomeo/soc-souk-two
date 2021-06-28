from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='assets_by_category_store'),
    path('category/<slug:category_slug>/<slug:asset_slug>/', views.asset_detail, name='asset_detail'),
    path('search/', views.search, name='search'),
    path('submit_comment/<int:asset_id>/', views.submit_comment, name='submit_comment'),
]