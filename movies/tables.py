from tables_pro.tables import *
from movies.models import Movie


class MovieTable1(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "homepage",
            "popularity",
            "release_date",
            "revenue",
            "runtime",
        )
        attrs = {"class": "table table-sm table-responsive table-hover hover-link"}


class MovieTable3(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "homepage",
            "popularity",
            "release_date",
            "revenue",
            "runtime",
        )
        attrs = {"class": "table table-sm table-responsive table-hover hover-link"}
        sequence = ("selection", "...")

    selection = SelectionColumn()
