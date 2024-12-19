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
    verification_code = models.CharField(default='2345', max_length=4)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


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
    description = models.TextField(blank=True, null=True)
    stay = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    tour_rules = models.TextField(blank=True, null=True)
    required_documents = models.TextField(blank=True, null=True)
    tour_services = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='tour/', null=True, blank=True)

    def __str__(self):
        return self.title


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_images')
    image = models.ImageField(upload_to='tour_images/', blank=True, null=True)

    def __str__(self):
        return self.tour.title


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passengers',null=True,blank=True)
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
