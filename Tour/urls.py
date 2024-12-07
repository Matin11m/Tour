from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import verify_code

router = DefaultRouter()
router.register(r'userprofile', views.UserProfileViewSet)

router.register(r'cities', views.CitiesViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tours', views.TourViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'favorites', views.FavoritesViewSet)
router.register(r'comments', views.CommentsViewSet)
router.register(r'passengers', views.PassengersViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'transactions', views.TransactionsViewSet)
router.register(r'refunds', views.RefundViewSet)
router.register(r'banners', views.BannerViewSet)
router.register(r'first_banners', views.FirstBannerViewSet)
router.register(r'city_banners', views.CityBannerViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
