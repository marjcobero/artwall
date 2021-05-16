from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:artwork_slug>/', views.artwork, name='artwork'),
    path('<slug:category_slug>/', views.category, name='category')
]