import django_filters

class SearchFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='discounted_price', lookup_expr='gt')