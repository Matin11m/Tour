from contextlib import nullcontext

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    phone_number_emergency = models.CharField(max_length=15, blank=True, null=True)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    marital_status = models.CharField(max_length=10, choices=[('single', 'Single'), ('married', 'Married')])
    card_number = models.CharField(max_length=16)
    iban = models.CharField(max_length=24)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f'{self.name}, {self.province.name}'


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description provided.")
    image = models.ImageField(upload_to='images_category/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tour(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='reports')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description provided.")
    stay = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(default="No additional details provided.")
    tour_rules = models.CharField(max_length=400, blank=True, null=True)
    required_documents = models.CharField(max_length=400, blank=True, null=True)
    tour_services = models.CharField(max_length=400, blank=True, null=True)
    image = models.ImageField(upload_to='tour/', null=True, blank=True)

    def __str__(self):
        return self.title


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_images')
    image = models.ImageField(upload_to='tour_images/', blank=True, null=True)

    def __str__(self):
        return self.tour


class TourReport(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reports')
    day = models.IntegerField()
    report = models.TextField()
    image = ImageField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return self.report


class Trip(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='trips')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capacity = models.PositiveIntegerField()
    duration = models.CharField(max_length=100, blank=True, null=True)
    stay = models.CharField(max_length=100, blank=True, null=True)
    trip_type = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    meal = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Trip for {self.tour.title}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user.username} - {self.tour.title}'


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments')
    score = models.IntegerField()
    visibility = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )

    def __str__(self):
        return f'{self.user.username} - {self.tour.title}'


class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    adults_number = models.PositiveIntegerField()
    children_number = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, default='pending')
    payment_status = models.CharField(max_length=50, default='unpaid')
    refund_status = models.CharField(max_length=50, default='not_requested')

    def __str__(self):
        return f'Order by {self.user.username} for {self.trip.tour.title}'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f'Transaction by {self.user.username} for {self.order}'


class Refund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refunds')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    text = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='requested')

    def __str__(self):
        return f'Refund requested by {self.user.username}'


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='header_banner/')
    link = models.URLField(max_length=200, blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class FirstBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='First_banners/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='first_banners')

    def __str__(self):
        return self.title


class CityBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='City_banners/')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='first_banners')

    def __str__(self):
        return self.title


# class Tour(models.Model):
# name = models.CharField(max_length=255)
# accommodation = models.CharField(max_length=255)
# tour_type = models.CharField(max_length=100)
# duration = models.CharField(max_length=150, null=True, blank=True)
# food = models.CharField(max_length=255)
# travel_month = models.CharField(max_length=50)
# time_period = models.CharField(max_length=100)
# capacity = models.IntegerField(null=True, blank=True)
# price = models.DecimalField(max_digits=10, decimal_places=2)
# accommodation_details = models.TextField()
# tour_services = models.TextField()
# tour_report = models.TextField()
# required_documents = models.TextField()
# tour_rules = models.TextField()
# passenger_comments = models.TextField()
# image = models.ImageField(upload_to='tour_images/')
#
# category = models.ForeignKey(Category, related_name='reports', on_delete=models.CASCADE)
# city = models.ForeignKey(Cities, related_name='reports', on_delete=models.CASCADE)
#
# def __str__(self):
#     return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     mobile_number = models.CharField(max_length=15, unique=True)
#     birth_date = models.DateField(null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"

# class BuyForm(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_forms')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     national_id = models.CharField(max_length=10)
#     birth_date = models.DateField()
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
#     tour = models.ForeignKey('Tour', related_name='buy_forms', on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.tour:
#             Reservation.objects.create(user=self.user, tour=self.tour, status='Pending')
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class BuyForm(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_forms')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     national_id = models.CharField(max_length=10)
#     birth_date = models.DateField()
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
#     tour = models.ForeignKey('Tour', related_name='buy_forms', on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.tour:
#             Reservation.objects.create(user=self.user, tour=self.tour, status='Pending')
#
#

#
#
# class TourImage(models.Model):
#     tour = models.ForeignKey(Tour, related_name='tour_images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='reports/tour_images/')
#
#     def __str__(self):
#         return f"Image for {self.tour.name}"
#
#
# class TourReport(models.Model):
#     tour = models.ForeignKey(Tour, related_name='reports', on_delete=models.CASCADE)
#     day = models.IntegerField()
#     report = models.TextField()
#     image = models.ImageField(upload_to='tour/reports/', blank=True, null=True)
#
#     def __str__(self):
#         return f"Day {self.day} of {self.tour.name}"
#
#
# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
#     tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='favorited_by')
#
#     class Meta:
#         unique_together = ('user', 'tour')
#
#     def __str__(self):
#         return f"{self.user.username} added {self.tour.name} to favorites"
#
#
# class Reservation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
#     tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
#     reservation_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50,
#                               choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
#
#     def __str__(self):
#         return f"{self.user.username} reserved {self.tour.name}"
