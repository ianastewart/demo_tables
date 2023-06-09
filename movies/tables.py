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

        attrs = {
            "class": "table table-sm table-hover hover-link",
            "thead": {"class": "bg-light border-top border-bottom"},
        }
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
        sequence = ("selection",)
        columns = {
            "fixed": ["selection", "title", "budget", "popularity"],
            "default": ["release_date"],
        }
        columns_md = {
            "fixed": ["selection", "title", "budget"],
        }
        columns_sm = {
            "fixed": ["selection", "title"],
        }
        responsive = {500: columns_sm, 768: columns_sm}

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()
