from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductHistoryViewSet, basename='Product')
router.register(r'favorites', views.FavoritesViewSet, basename='Favorites')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
