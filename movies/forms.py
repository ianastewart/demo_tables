from django import forms
from django.forms.widgets import CheckboxInput

from .models import Movie
from django_tableaux.models import Pagination, FilterStyle, ClickAction

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "revenue",
            "vote_count",
        ]


class BasicSettingsForm(forms.Form):
    row_settings = forms.BooleanField(required=False)
    column_settings = forms.BooleanField(required=False)
    column_reset = forms.BooleanField(required=False)
    sticky_header = forms.BooleanField(required=False)
    fixed_width = forms.BooleanField(required=False)
    indicator = forms.BooleanField(required=False)
    # page_settings = forms.ChoiceField(
    #     choices=(("none", "No paging"), ("paged", "Paged"), ("infinite", "Infinite scroll"),
    #              ("load", "Infinite load more")), required=False)
    pagination = forms.ChoiceField(choices=Pagination.choices, required=False)
    filter_style = forms.ChoiceField(choices=FilterStyle.choices, required=False)
    filter_pills = forms.BooleanField(required=False)
    filter_button = forms.BooleanField(required=False)
    click_action = forms.ChoiceField(choices=ClickAction.choices, required=False)
    fixed_height = forms.ChoiceField(choices=((0, "Not fixed"), (300, "300px"), (600, "600px")), required=False)
