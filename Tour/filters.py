from django_filters import rest_framework as filters
from Tour.models import Tour


class TourFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="trips__price", lookup_expr='gte', label="Minimum Price")
    max_price = filters.NumberFilter(field_name="trips__price", lookup_expr='lte', label="Maximum Price")

    class Meta:
        model = Tour
        fields = ['city', 'min_price', 'max_price']
