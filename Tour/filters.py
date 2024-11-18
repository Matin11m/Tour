from django_filters import rest_framework as filters
from unicodedata import category

from Tour.models import Tour, Comment, UserProfile


class TourFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="trips__price", lookup_expr='gte', label="Minimum Price")
    max_price = filters.NumberFilter(field_name="trips__price", lookup_expr='lte', label="Maximum Price")
    start_date = filters.DateFilter(field_name="trips__start_date", lookup_expr='gte', label="Start Date")
    end_date = filters.DateFilter(field_name="trips__start_date", lookup_expr='lte', label="End Date")
    capacity = filters.NumberFilter(field_name="trips__capacity", lookup_expr='gt', label="Capacity")
    category = filters.CharFilter(field_name="category__title", lookup_expr='exact', label="Category")

    # Search:
    city = filters.CharFilter(field_name="city__name", lookup_expr='icontains', label="Search City")

    CITY_CHOICES = [
        ('تهران', 'تهران'),
        ('یزد', 'یزد'),
        ('اصفهان', 'اصفهان'),
        ('مشهد', 'مشهد'),
        ('اردبیل', 'اردبیل'),
        ('کیش', 'کیش'),
        ('رامسر', 'رامسر'),
        ('قشم', 'قشم'),
    ]

    city_filter = filters.ChoiceFilter(field_name="city__name", choices=CITY_CHOICES, label="City")


class Meta:
    model = Tour
    fields = ['city_filter', 'city', 'min_price', 'max_price', 'category', 'start_date', 'end_date', ]


class CommentFilter(filters.FilterSet):
    tour_name = filters.CharFilter(field_name='tour__title', lookup_expr='icontains', label="Tour Name")
    start_date = filters.DateFilter(field_name="tour__trips__start_date", lookup_expr='gte', label="Start Date")
    end_date = filters.DateFilter(field_name="tour__trips__start_date", lookup_expr='lte', label="End Date")

    class Meta:
        model = Comment
        fields = ['tour_name', 'start_date', 'end_date', ]


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains', label="First Name")
    last_name = filters.CharFilter(lookup_expr='icontains', label="Last Name")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']
