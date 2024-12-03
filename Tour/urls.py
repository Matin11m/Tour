# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CategoryViewSet, TourViewSet, BuyFormViewSet, FavoriteViewSet, ReservationViewSet
#
# router = DefaultRouter()
# router.register(r'categories', views.CategoryViewSet, basename='category')
# router.register(r'reports', views.TourViewSet, basename='tour')
# router.register(r'buy_forms', views.BuyFormViewSet)
# router.register(r'favorites', views.FavoriteViewSet)
# router.register(r'reservations', views.ReservationViewSet)
# # router.register(r'register', views.RegisterViewSet, basename='register')
# # router.register(r'login', views.LoginViewSet, basename='login')
#
# urlpatterns = [
#     path('', views.include(router.urls)),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'userprofiles', views.UserProfileViewSet)
# router.register(r'provinces', views.ProvinceViewSet)
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
    path('send-sms/', views.send_sms),
    path('verify-code/', views.verify_code),
 ]
