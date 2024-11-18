# from rest_framework import serializers
# from .models import Tour, Category, TourImage, TourReport, Favorite, BuyForm, Reservation
# from django.contrib.auth import authenticate
#
#
#
# class BuyFormSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BuyForm
#         fields = ['id', 'user', 'first_name', 'last_name', 'national_id', 'birth_date', 'gender', 'tour', 'created_at']
#
#
# class TourReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TourReport
#         fields = ['id', 'day', 'report', 'image']
#
#
# class TourImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TourImage
#         fields = ['id', 'image']
#
#
# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = ['id', 'user', 'tour', 'reservation_date', 'status']
#
#
# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ['id', 'user', 'tour']
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']
#
#
# class TourSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     tour_images = TourImageSerializer(many=True, read_only=True)
#     reports = TourReportSerializer(many=True, read_only=True)
#     buy_forms = BuyFormSerializer(many=True, read_only=True)
#     reservations = ReservationSerializer(many=True, read_only=True)
#
#     is_favorite = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Tour
#         fields = ['id', 'name', 'accommodation', 'tour_type', 'duration', 'food', 'travel_month', 'time_period',
#                   'capacity', 'price', 'accommodation_details', 'tour_services', 'tour_report', 'required_documents',
#                   'tour_rules', 'passenger_comments', 'image', 'category', 'tour_images', 'reports', 'buy_forms',
#                   'reservations', 'is_favorite']
#
#     def create(self, validated_data):
#         category_data = validated_data.pop('category')
#         reports_data = self.context['request'].data.get('reports', [])
#         image_data = self.context['request'].data.get('tour_images', [])
#
#         category, created = Category.objects.get_or_create(name=category_data['name'])
#         tour = Tour.objects.create(category=category, **validated_data)
#
#         if image_data:
#             TourImage.objects.bulk_create([TourImage(tour=tour, image=image) for image in image_data])
#
#         if reports_data:
#             TourReport.objects.bulk_create([TourReport(
#                 tour=tour,
#                 day=report.get('day'),
#                 report=report.get('report'),
#                 image=report.get('image')
#             ) for report in reports_data])
#
#         return tour
#
#     def get_is_favorite(self, obj):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return Favorite.objects.filter(user=user, tour=obj).exists()
#         return False
#
# #
# # from django.contrib.auth.models import User
# # from rest_framework import serializers
# # # from .models import Profile
#
#
# # class ProfileSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Profile
# #         fields = ('mobile_number', 'birth_date',)
#
#
# # class UserSerializer(serializers.ModelSerializer):
# #     profile = ProfileSerializer()
# #
# #     class Meta:
# #         model = User
# #         fields = ('id', 'username', 'password', 'profile')
# #         extra_kwargs = {'password': {'write_only': True}}
# #
# #     def create(self, validated_data):
# #         profile_data = validated_data.pop('profile')
# #         user = User.objects.create(username=validated_data['username'])
# #         user.set_password(validated_data['password'])
# #         user.save()
# #         Profile.objects.create(user=user, **profile_data)
# #         return user


from rest_framework import serializers
from .models import UserProfile, Province, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
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


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitiesSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)  # نمایش جزئیات استان مربوطه

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


class TourSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
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
