from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TourViewSet, BuyFormViewSet, FavoriteViewSet, ReservationViewSet, RegisterViewSet, \
    LoginViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'buy_forms', BuyFormViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]