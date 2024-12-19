from django.contrib.auth import get_user_model
from random import randint
from rest_framework import viewsets
from django.db.utils import IntegrityError
from Tour.helpers import send_otp
from .models import UserProfile, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund, Banner, FirstBanner, CityBanner
from .serializers import UserProfileSerializer, CitiesSerializer, CategorySerializer, \
    TourSerializer, TripSerializer, FavoritesSerializer, CommentsSerializer, PassengersSerializer, OrderSerializer, \
    TransactionsSerializer, RefundSerializer, BannerSerializer

from Tour.filters import TourFilter, CommentFilter, UserFilter

User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_class = UserFilter


# class ProvinceViewSet(viewsets.ModelViewSet):
#     queryset = Province.objects.all()  # اصلاح نام مدل به Province
#     serializer_class = ProvinceSerializer  # اصلاح نام سریالایزر به ProvinceSerializer
#

class CitiesViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitiesSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filterset_class = TourFilter


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    filterset_class = CommentFilter


# class PassengersViewSet(viewsets.ModelViewSet):
#     queryset = Passenger.objects.all()
#     serializer_class = PassengersSerializer
class PassengersViewSet(viewsets.ModelViewSet):
    serializer_class = PassengersSerializer

    def get_queryset(self):
        return Passenger.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class FirstBannerViewSet(viewsets.ModelViewSet):
    queryset = FirstBanner.objects.all()
    serializer_class = BannerSerializer


class CityBannerViewSet(viewsets.ModelViewSet):
    queryset = CityBanner.objects.all()
    serializer_class = BannerSerializer


# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from drf_yasg import openapi
#
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import IntegrityError
from Tour.models import UserProfile


# @swagger_auto_schema(
#     method='post',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
#         },
#         required=['phone'],
#     ),
#     responses={200: openapi.Response('Successful Response', openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
#         },
#     ))}
# )
@api_view(['POST'])
def send_sms(request):
    phone = request.data.get('phone')
    if phone and request.user.is_anonymous:
        verification_code_number = randint(1000, 9999)
        verification_code = str(verification_code_number)
        user = None
        try:
            user = User.objects.create_user(username=phone)
            UserProfile.objects.create(
                user=user,
                phone_number=phone,
                verification_code=verification_code
            )
        except IntegrityError:
            user = User.objects.get(username=phone)
            user.profile.verification_code = verification_code
            user.profile.save()
        # TODO: handle errors
        send_otp(phone, verification_code)
        return Response({'message': 'Waiting to receive verification code!'})
    return Response({'message': 'fill phone number'})


# @swagger_auto_schema(
#     method='post',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
#             'code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification code'),
#         },
#         required=['phone', 'code'],
#     ),
#     responses={200: openapi.Response('Successful Response', openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
#         },
#     ))}
# )
@api_view(['POST'])
def verify_code(request):
    # TODO: handle errors
    phone = request.data.get('phone')
    code = request.data.get('code')
    profile = UserProfile.objects.get(
        user__username=phone,
        verification_code=code
    )
    refresh = RefreshToken.for_user(profile.user)
    return Response({
        'refresh': str(refresh),  # تبدیل شیء RefreshToken به رشته
        'access': str(refresh.access_token),  # دریافت access token به صورت رشته
    }, status=status.HTTP_200_OK)
