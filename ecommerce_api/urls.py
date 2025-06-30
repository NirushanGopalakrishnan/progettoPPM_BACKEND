from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticazione con djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Le tue app API
    path('api/store/', include('store.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
]

