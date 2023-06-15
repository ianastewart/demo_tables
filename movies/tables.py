import django_tables2 as tables
from tables_pro.columns import CurrencyColumn, RightAlignedColumn, SelectionColumn
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

        columns_lg = {
            "fixed": ["selection", "title", "budget", "popularity"],
        }
        columns_md = {
            "fixed": ["selection", "title", "budget"],
            "default": ["selection", "title", "budget"],
        }
        columns_sm = {
            "fixed": ["selection", "title"],
            "default": ["selection", "title"],
        }
        responsive = {300: columns_sm, 768: columns_md, 1000: columns_lg}

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()
