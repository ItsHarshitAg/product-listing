from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('api/products/', views.product_list, name='product_list'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('api/cart/', views.get_cart, name='get_cart'),
    path('api/checkout/', views.checkout, name='checkout'),
]
