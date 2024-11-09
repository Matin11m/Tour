# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
#
# from .models import Tour, Category
# from .serializers import TourSerializer, CategorySerializer, BuyFormSerializer, FavoriteSerializer, \
#     ReservationSerializer
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from kavenegar import KavenegarAPI
# import random
# # from .serializers import UserSerializer
#
#
# class TourViewSet(viewsets.ModelViewSet):
#     queryset = Tour.objects.all()
#     serializer_class = TourSerializer
#
#     def get_serializer_context(self):
#         context = super(TourViewSet, self).get_serializer_context()
#         context['request'] = self.request
#         return context
#
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def toggle_favorite(self, request, pk=None):
#         tour = self.get_object()
#         user = request.user
#
#         favorite, created = Favorite.objects.get_or_create(user=user, tour=tour)
#
#         if created:
#             return Response({'message': 'Tour added to favorites'}, status=status.HTTP_201_CREATED)
#         else:
#             favorite.delete()
#             return Response({'message': 'Tour removed from favorites'}, status=status.HTTP_200_OK)
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class BuyFormViewSet(viewsets.ModelViewSet):
#     queryset = BuyForm.objects.all()
#     serializer_class = BuyFormSerializer
#
#     # permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class FavoriteViewSet(viewsets.ModelViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer
#
#     def get_queryset(self):
#         return Favorite.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class ReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#
#     # permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Reservation.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# #
# #
# #
# # KAVEHNEGAR_API_KEY = '4B62615166304E675971316967436E47616B4E47433439385772663746455671634D323775554C2B4A63593D'
#
#
# # class RegisterViewSet(viewsets.ViewSet):
# #     def create(self, request):
# #         serializer = UserSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save()
# #
# #
# #             verification_code = str(random.randint(100000, 999999))
# #
# #
# #             mobile_number = serializer.validated_data['profile']['mobile_number']
# #             try:
# #                 api = KavenegarAPI(KAVEHNEGAR_API_KEY)
# #                 params = {
# #                     'receptor': mobile_number,
# #                     'token': verification_code,
# #                     'template': 'YourTemplateName',
# #                     'type': 'sms',
# #                 }
# #                 api.verify_lookup(params)
# #             except Exception as e:
# #                 return Response({"error": "SMS service failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# #
# #             return Response({"message": "Verification code sent to mobile number."}, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class LoginViewSet(viewsets.ViewSet):
# #     def create(self, request):
# #         mobile_number = request.data.get('mobile_number')
# #         password = request.data.get('password')
# #
# #         try:
# #             profile = Profile.objects.get(mobile_number=mobile_number)
# #             user = profile.user
# #             if user.check_password(password):
# #                 return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
# #             else:
# #                 return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
# #         except Profile.DoesNotExist:
# #             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets
from .models import UserProfile, Province, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund, Banner, FirstBanner, CityBanner
from .serializers import UserProfileSerializer, ProvinceSerializer, CitiesSerializer, CategorySerializer, \
    TourSerializer, TripSerializer, FavoritesSerializer, CommentsSerializer, PassengersSerializer, OrderSerializer, \
    TransactionsSerializer, RefundSerializer, BannerSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()  # اصلاح نام مدل به Province
    serializer_class = ProvinceSerializer  # اصلاح نام سریالایزر به ProvinceSerializer


class CitiesViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitiesSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class PassengersViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengersSerializer


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
