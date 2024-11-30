from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, CitiesViewSet, CategoryViewSet, TourViewSet, TripViewSet, \
    FavoritesViewSet, CommentsViewSet, PassengersViewSet, OrderViewSet, TransactionsViewSet, RefundViewSet, \
    BannerViewSet, FirstBannerViewSet, CityBannerViewSet

router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet)
router.register(r'cities', CitiesViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tours', TourViewSet)
router.register(r'trips', TripViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'passengers', PassengersViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionsViewSet)
router.register(r'refunds', RefundViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'first_banners', FirstBannerViewSet)
router.register(r'city_banners', CityBannerViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
