from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
# router.register('register/', views.UserRegistrationApiView.as_view(), basename='register')
router.register('register', views.UserRegistrationViewSet, basename='register')
# router.register('logout/', views.UserLogoutView.as_view(), basename='logout')

router.register('reviews', views.ReviewViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('products/active/<uid64>/<token>/', views.activate, name = 'activate'),
    # path('wishlist/', include('wishlist.urls')),
    # path('register/', views.UserRegistrationApiView.as_view()),
]