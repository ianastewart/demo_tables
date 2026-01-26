import django_tables2 as tables
from django_tableaux.columns import CurrencyColumn, RightAlignedColumn, SelectionColumn
from movies.models import Movie


class MovieTable(tables.Table):
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
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()


class MovieTableSelection(tables.Table):
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
        sequence = ("selection",)
        # attrs = {
        #     "class": "table table-sm table-hover hover-link",
        #     "thead": {"class": "bg-light border-top border-bottom"},
        # }

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    runtime = RightAlignedColumn()


class MovieTableResponsive(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "popularity",
            "release_date",
            "revenue",
            "runtime",
            "movie_status",
        )
        # sequence = ("selection",)
        attrs = {"class": "table table-sm table-hover hover-link",
                 "th": {"class": "bg-dark text-white no-wrap"},
                 }

        columns_xl = {
            "fixed": ["selection", "title", "budget", "popularity", "release_date", "runtime", "movie_status"],
        }

        columns_lg = {
            "fixed": ["selection", "title", "budget", "popularity", "release_date"],
            "default": [
                "selection",
                "title",
                "budget",
                "popularity",
                "release_date",
            ],
        }
        columns_md = {
            "fixed": ["selection", "title", "budget", "popularity"],
            "default": ["selection", "title", "budget", "popularity"],
        }
        columns_sm = {
            "fixed": ["selection", "title"],
            "default": ["selection", "title", "budget", "popularity"],
            "mobile": True,
            "attrs": {"th": "strong bg-dark text-white", "tr": "bg-light"},
        }
        responsive = {"sm": columns_sm, "md": columns_md, "lg": columns_lg, "xl": columns_xl}

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
    popularity = RightAlignedColumn()
    runtime = RightAlignedColumn()


class MovieTable4(tables.Table):
    class Meta:
        model = Movie
        fields = (
            "title",
            "budget",
            "popularity",
            "release_date",
            "revenue",
            "vote_count",
            "movie_status",
        )
        editable = [
            "vote_count",
        ]
        attrs = {"class": "table table-sm table-hover hover-link"}

    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(attrs={"td": {"class": "td_edit"}})
    runtime = RightAlignedColumn()
    vote_count = tables.Column()
