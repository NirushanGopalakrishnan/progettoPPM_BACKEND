from django.contrib import admin
from django.urls import path, include
from .views import index  # importa la nuova view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', index, name='index'),

    # Autenticazione con djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Le tue app API
    path('api/store/', include('store.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
]

