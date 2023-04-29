from tables_pro.tables import *
from movies.models import Movie


class MovieTable1(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "popularity",
            "release_date",
            "revenue",
            "runtime",
        )
        attrs = {"class": "table table-sm table-hover hover-link",
                 "thead":{"class": "bg-light border-top border-bottom"}}
        # row_attrs = {"th": {"class": "bg-dark"}}

    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()


class MovieTable3(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "popularity",
            "release_date",
            "revenue",
            "runtime",
        )
        attrs = {"class": "table table-sm table-hover hover-link"}
        sequence = ("selection", "...")

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()