import django_filters
from .models import profile

class CharArrayFilter(django_filters.Filter):
    field_class = django_filters.CharFilter

    def filter(self, qs, value):
        if not value:
            return qs
        values = value.split(',')
        filter_kwargs = {f'{self.field_name}__in': values}
        return qs.filter(**filter_kwargs)

class ProfileFilter(django_filters.FilterSet):
    category_name = CharArrayFilter(
        field_name='category__name',
        lookup_expr='icontains',
    )
    platform_name = CharArrayFilter(
        field_name='platform__name',
        lookup_expr='icontains',
    )

    min_price = django_filters.NumberFilter(
        field_name='game_price', 
        lookup_expr='gte'
    )

    max_price = django_filters.NumberFilter(
        field_name='game_price', 
        lookup_expr='lte'
    )

    class Meta:
        model = profile
        fields = ['category_name', 'platform_name', 'min_price', 'max_price']