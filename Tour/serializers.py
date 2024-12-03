from rest_framework import serializers
from unicodedata import category

from .models import UserProfile, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund, Banner, FirstBanner, CityBanner, TourImage, TourReport
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'first_name', 'last_name', 'phone_number', 'phone_number_emergency', 'national_id',
            'birth_date', 'gender', 'marital_status', 'card_number', 'iban']


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


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


class TripSerializer(serializers.ModelSerializer):
    tour_title = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'id', 'tour_title', 'price', 'discount_price', 'capacity',
            'duration', 'stay', 'trip_type', 'start_date',
            'end_date', 'meal'
        ]

    def get_tour_title(self, obj):
        return obj.tour.title


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image']


class TourReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourReport
        fields = ['id', 'day', 'report', 'image']


class TourSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    city = CitiesSerializer(read_only=True)
    trip = TripSerializer(read_only=True)
    tour_images = TourImageSerializer(many=True, read_only=True)
    reports = TourReportSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id', 'category', 'city', 'title', 'description', 'stay',
            'details', 'tour_rules', 'required_documents',
            'tour_services', 'image']


class FavoritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'tour']


class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tour = TourSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'tour', 'score', 'visibility']


class PassengersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Passenger
        fields = ['id', 'user', 'first_name', 'last_name', 'national_id', 'birth_date', 'gender']


class OrderSerializer(serializers.ModelSerializer):
    passenger = PassengersSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    trip = TripSerializer

    class Meta:
        model = Order
        fields = ['id', 'passenger', 'user', 'trip', 'price', 'adults_number', 'children_number', 'order_status',
                  'payment_status', 'refund_status']


class TransactionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'order', 'amount', 'transaction_details', 'status']


class RefundSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Refund
        fields = ['id', 'user', 'order', 'text', 'refund_amount', 'status']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'link']


class FirstBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstBanner
        fields = ['id', 'title', 'image', 'category']


class CityBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityBanner
        fields = ['title', 'image', 'city']
