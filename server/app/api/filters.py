import django_filters
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from .models import Product


class ProductFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        field_name = 'type',
        choices = Product.PRODUCT_TYPES,
        lookup_expr = 'iexact'
    )

    price_min = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'gte')
    price_max = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'lt')

    created_after = django_filters.IsoDateTimeFilter(field_name = 'created_at', lookup_expr = 'gte')
    created_before = django_filters.IsoDateTimeFilter(field_name = 'created_at', lookup_expr = 'lte')

    name = django_filters.CharFilter(method = 'filter_by_name')
    tag = django_filters.CharFilter(field_name = 'producttag__tag__slug', lookup_expr = 'iexact')

    def filter_by_name(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .annotate(similarity = TrigramSimilarity('name', value))
            .filter(Q(name__icontains = value) | Q(similarity__gt = 0.2))
            .order_by('-similarity', 'name')
        )

    class Meta:
        model = Product
        fields = ['type', 'price_min', 'price_max', 'name', 'tag']
