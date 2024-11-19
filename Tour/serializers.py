from rest_framework import serializers
from .models import UserProfile, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund, Banner, FirstBanner, CityBanner
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش اطلاعات کاربر به صورت تودرتو

    class Meta:
        model = UserProfile
        fields = '__all__'


# class ProvinceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Province
#         fields = '__all__'


class CitiesSerializer(serializers.ModelSerializer):
    # province = ProvinceSerializer(read_only=True)

    class Meta:
        model = City
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'image', 'parent']

    def get_parent(self, obj):
        return obj.parent.title if obj.parent else None


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TourSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)  # نمایش تور مرتبط

    class Meta:
        model = Trip
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش اطلاعات کاربر مرتبط
    tour = TourSerializer(read_only=True)  # نمایش تور مورد علاقه

    class Meta:
        model = Favorite
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش اطلاعات کاربر
    tour = TourSerializer(read_only=True)  # نمایش تور مرتبط

    class Meta:
        model = Comment
        fields = '__all__'


class PassengersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش کاربر مرتبط

    class Meta:
        model = Passenger
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    passenger = PassengersSerializer(read_only=True)  # نمایش اطلاعات مسافر
    user = UserSerializer(read_only=True)  # نمایش اطلاعات کاربر
    trip = TripSerializer(read_only=True)  # نمایش جزئیات سفر

    class Meta:
        model = Order
        fields = '__all__'


class TransactionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش کاربر مرتبط
    order = OrderSerializer(read_only=True)  # نمایش اطلاعات سفارش

    class Meta:
        model = Transaction
        fields = '__all__'


class RefundSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # نمایش کاربر مرتبط
    order = OrderSerializer(read_only=True)  # نمایش سفارش مرتبط

    class Meta:
        model = Refund
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class FirstBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstBanner
        fields = '__all__'


class CityBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityBanner
        fields = '__all__'
