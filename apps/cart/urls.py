from django.urls import path
from . import views


urlpatterns = [
    path('cart', views.cart_detail, name='cart'),
    path('success/', views.success, name='success')
]