from django.urls import path
from .views import ProductListCreateView, CartView, AddToCartView, UpdateCartQuantityView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='products-list-create'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/update-quantity/', UpdateCartQuantityView.as_view(), name='cart-update-quantity'),
]
