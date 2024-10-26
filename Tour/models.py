from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BuyForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_forms')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    tour = models.ForeignKey('Tour', related_name='buy_forms', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tour:
            Reservation.objects.create(user=self.user, tour=self.tour, status='Pending')


class Tour(models.Model):
    name = models.CharField(max_length=255)
    accommodation = models.CharField(max_length=255)
    tour_type = models.CharField(max_length=100)
    duration = models.CharField(max_length=150, null=True, blank=True)
    food = models.CharField(max_length=255)
    travel_month = models.CharField(max_length=50)
    time_period = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    accommodation_details = models.TextField()
    tour_services = models.TextField()
    tour_report = models.TextField()
    required_documents = models.TextField()
    tour_rules = models.TextField()
    passenger_comments = models.TextField()
    image = models.ImageField(upload_to='images/')

    category = models.ForeignKey(Category, related_name='tours', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tours/images/')

    def __str__(self):
        return f"Image for {self.tour.name}"


class TourReport(models.Model):
    tour = models.ForeignKey(Tour, related_name='reports', on_delete=models.CASCADE)
    day = models.IntegerField()
    report = models.TextField()
    image = models.ImageField(upload_to='tour/reports/', blank=True, null=True)

    def __str__(self):
        return f"Day {self.day} of {self.tour.name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'tour')

    def __str__(self):
        return f"{self.user.username} added {self.tour.name} to favorites"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,
                              choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])

    def __str__(self):
        return f"{self.user.username} reserved {self.tour.name}"
