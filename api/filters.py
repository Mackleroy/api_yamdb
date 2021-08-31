import django_filters

from api.models import Title


class GenreCategoryFilter(django_filters.FilterSet):
    """Filter by ForeignKey Slug of Genre and Category, also name containing and year"""
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['year', 'name']
