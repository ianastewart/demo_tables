from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    ModelChoiceFilter,
    RangeFilter,
)
from movies.models import Movie


# noinspection PyUnusedLocal
class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = ["title"]

    title = CharFilter(field_name="title", lookup_expr="icontains")
    budget = RangeFilter(field_name="budget")
