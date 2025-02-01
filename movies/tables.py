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
        attrs = {
            # "class": "table table-sm table-hover",
            # "thead": {"class": "border-top border-bottom sticky "},
            # "th": {"class": "border-top border-bottom sticky"},
        }

    budget = CurrencyColumn(prefix="$", attrs={"class": "bg-danger"})
    revenue = CurrencyColumn(prefix="$")
    # runtime = RightAlignedColumn()
    runtime = tables.Column()


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
        attrs = {
            "class": "table table-sm table-hover hover-link",
            "thead": {"class": "bg-light border-top border-bottom"},
        }

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
        )
        # sequence = ("selection",)
        # attrs = {"class": "table table-sm table-hover hover-link"}

        columns_lg = {
            "fixed": ["selection", "title", "budget", "popularity"],
        }
        columns_md = {
            "fixed": ["selection", "title", "budget"],
            "default": ["selection", "title", "budget"],
        }
        columns_sm = {
            "fixed": ["selection", "title"],
            "default": ["selection", "title", "budget", "popularity"],
            "mobile": True,
            "attrs": {"th": "strong bg-dark text-white", "tr": "bg-light"},
        }
        responsive = {300: columns_sm, 600: columns_md, 900: columns_lg}

    selection = SelectionColumn()
    budget = CurrencyColumn(prefix="$")
    revenue = CurrencyColumn(prefix="$")
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
