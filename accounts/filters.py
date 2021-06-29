import django_filters

from django_filters import CharFilter, NumberFilter

from .models import *


class FlightFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains',label='航班号')
    price = NumberFilter(field_name='price', lookup_expr='lte', label="Price<=")
    start = CharFilter(field_name='start', label='起点')
    end = CharFilter(field_name='end', label='到达')

    class Meta:
        model = Flight
        fields = '__all__'
        exclude = ['capacity', 'purchased', 'departureTime', 'columnnum', 'rownum']
