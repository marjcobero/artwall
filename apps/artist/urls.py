from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('join/', views.join, name='join'),
    path('artist-admin/', views.artist_admin, name='artist_admin'),
    path('add-artwork/', views.add_artwork, name='add_artwork'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='artist/login.html'), name='login'),
    path('', views.artists, name='artists'),
    path('<int:artist_id>/', views.artist, name='artist'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]