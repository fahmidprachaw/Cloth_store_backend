from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()
router.register('', views.WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('items/', views.WishlistItemsAPIView.as_view(), name='wishlist-items'),
    path('add/', views.AddToWishlistAPIView.as_view(), name='add-to-wishlist'),
    path('', include(router.urls)),
]