from django.urls import path
from .views import ProductListCreateView, CartView, AddToCartView, UpdateCartQuantityView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/update-quantity/', UpdateCartQuantityView.as_view(), name='update-cart-quantity'),
]
