from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    ModelChoiceFilter,
    RangeFilter,
    NumberFilter,
)
from django_filters.widgets import DateRangeWidget
from django import forms
from django_flatpickr.widgets import DatePickerInput

from movies.models import Movie


class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = ["title"]

    title = CharFilter(field_name="title", lookup_expr="icontains")
    budget = NumberFilter(field_name="budget", lookup_expr="gt")
    release_date = DateFilter(field_name="release_date",lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    #release_date = DateFilter(field_name="release_date",lookup_expr="gte", widget=DatePickerInput())
