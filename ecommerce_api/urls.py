from django.contrib import admin
from django.urls import path, include
from ecommerce_api.views import index  # importa la view index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/store/', include('store.urls')),  # Solo store
    path('', index, name='index'),  # root URL punta alla view index
]
