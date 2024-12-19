from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        fields = ['id', 'day', 'report', 'image', ]


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
            'tour_services', 'reports', 'image', 'tour_images', 'trip']


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
    user = UserSerializer(allow_null=True)

    class Meta:
        model = Passenger
        fields = ['id', 'user', 'first_name', 'last_name', 'national_id', 'birth_date', 'gender']

# class PassengersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Passenger
#         fields = ['id', 'user', 'first_name', 'last_name', 'national_id', 'birth_date', 'gender']
#         extra_kwargs = {'user': {'read_only': True}}
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         validated_data['user'] = request.user
#         return super().create(validated_data)



class OrderSerializer(serializers.ModelSerializer):
    passenger = PassengersSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    trip = serializers.SerializerMethodField()
    trip_duration = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['passenger', 'user', 'trip', 'price', 'adults_number', 'children_number', 'order_status',
                  'payment_status', 'refund_status', 'trip_duration']

    def get_trip(self, obj):
        return obj.trip.tour.title if obj.trip and obj.trip.tour else None

    def get_trip_duration(self, obj):
        return obj.trip.duration if obj.trip else None


class TransactionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    trip_start_date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'order', 'trip_start_date', 'transaction_details', 'status']

    def get_trip_start_date(self, obj):
        if obj.order and obj.order.trip:
            return obj.order.trip.start_date
        return None


class RefundSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    card_number = serializers.SerializerMethodField()
    iban = serializers.SerializerMethodField()

    class Meta:
        model = Refund
        fields = ['id', 'user', 'order', 'text', 'refund_amount', 'status', 'iban', 'card_number']

    def get_card_number(self, obj):
        if obj.user and hasattr(obj.user, 'profile'):
            return obj.user.profile.card_number
        return None

    def get_iban(self, obj):
        if obj.user and hasattr(obj.user, 'profile'):
            return obj.user.profile.iban
        return None


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'link']


class FirstBannerSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = FirstBanner
        fields = ['id', 'title', 'image', 'category']

    def validate(self, data):
        if FirstBanner.objects.count() >= 3 and self.instance is None:
            raise ValidationError("فقط می‌توانید ۳ بنر اضافه کنید.")
        return data


class CityBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityBanner
        fields = ['title', 'image', 'city']
