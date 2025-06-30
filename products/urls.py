from django.urls import path
from .views import ProductListCreateView, CartView, AddToCartView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
]
