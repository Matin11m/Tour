from rest_framework import serializers
from .models import UserProfile, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund, Banner, FirstBanner, CityBanner
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


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


class TripSerializer:
    class Meta:
        model = Trip
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    trip = TripSerializer

    class Meta:
        model = Tour
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PassengersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Passenger
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    passenger = PassengersSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    trip = TripSerializer

    class Meta:
        model = Order
        fields = '__all__'


class TransactionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class RefundSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

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
