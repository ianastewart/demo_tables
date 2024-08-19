from django.shortcuts import render, reverse
from django.views.generic import ListView, TemplateView, DetailView
from django_htmx.http import (
    HttpResponseClientRedirect,
    retarget,
)
from django_tableaux.views import TableauxView, SelectedMixin

from .filters import MovieFilter
from .forms import MovieForm
from .models import Movie
from .tables import MovieTable, MovieTableSelection, MovieTableResponsive, MovieTable4


class MoviesListView(ListView):
    model = Movie
    template_name = "movies/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.all().order_by("title")
        return context


class BasicView(TableauxView):
    title = "Basic view"
    caption = "This table has a caption"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie


class RowColSettingsView(TableauxView):
    title = "Row and column settings"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    row_settings = True
    column_settings = True
    sticky_header = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["css_toolbar"] = "bg-light"
        context["css_table"] = "bg-white"
        return context


class SelectActionsView(TableauxView):
    title = "Selection and actions"
    table_class = MovieTableSelection
    template_name = "movies/table.html"
    model = Movie

    def get_bulk_actions(self):
        return (
            ("action_message", "Action with message"),
            ("action_modal", "Action in a modal"),
            ("action_page", "Action on a new page"),
            ("export", "Export to csv"),
            ("export_xlsx", "Export as xlsx"),
        )

    def handle_action(self, request, action):
        if action == "action_message":
            context = {
                "message": f"Action on {self.selected_objects.count()} rows",
                "alert_class": "alert-success",
            }
            response = render(request, self.templates["alert"], context)
            return retarget(response, "#messages")

        elif action == "action_modal":
            context = {"selected": self.selected_objects}
            return render(request, "movies/action_modal.html", context)

        elif action == "action_page":
            request.session["selected_ids"] = self.selected_ids
            path = reverse("action_page") + request.POST["query"]
            return HttpResponseClientRedirect(path)


class ActionPageView(SelectedMixin, TemplateView):
    model = Movie
    filterset_class = MovieFilter
    template_name = "movies/action_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = self.get_query_set()
        return context


class InfiniteScollView(TableauxView):
    title = "Infinite scroll"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    infinite_scroll = True
    sticky_header = True


class InfiniteLoadView(TableauxView):
    title = "Infinite load more"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    infinite_load = True
    sticky_header = True


class MoviesFilterToolbarView(TableauxView):
    title = "Filter toolbar"
    table_class = MovieTable
    filterset_class = MovieFilter
    filter_style = TableauxView.FilterStyle.TOOLBAR
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    model = Movie


class MoviesFilterModalView(SelectActionsView):
    title = "Filter modal"
    table_class = MovieTableResponsive
    filterset_class = MovieFilter
    filter_style = TableauxView.FilterStyle.MODAL
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    model = Movie


class MoviesFilterHeaderView(SelectActionsView):
    title = "Filter in header"
    table_class = MovieTableResponsive
    filterset_class = MovieFilter
    filter_style = TableauxView.FilterStyle.HEADER
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    # responsive = True


class MoviesEditableView(TableauxView):
    title = "Editable columns"
    model = Movie
    form_class = MovieForm
    table_class = MovieTable4
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True


class MoviesRowClickView(TableauxView):
    title = "Click row shows detail page"
    template_name = "movies/table.html"
    table_class = MovieTable
    model = Movie
    click_action = TableauxView.ClickAction.GET
    click_url_name = "movie_detail"


class MoviesRowClickModalView(TableauxView):
    title = "Click row shows detail modal "
    template_name = "movies/table.html"
    table_class = MovieTableResponsive
    model = Movie
    click_action = TableauxView.ClickAction.HX_GET
    click_url_name = "movie_modal"


class MoviesRowClickCustomView(TableauxView):
    title = "Custom click cell"
    template_name = "movies/table.html"
    table_class = MovieTableResponsive
    model = Movie
    click_action = TableauxView.ClickAction.CUSTOM

    def cell_clicked(self, pk, column_name, target):
        movie = Movie.objects.get(pk=pk)
        context = {
            "message": f"'{movie.title}', primary key: {pk}, column: {column_name} was clicked.",
            "alert_class": "alert-success",
        }
        response = render(
            self.request, "django_tableaux/bootstrap4/alert.html", context
        )
        return retarget(response, "#messages")


class MovieDetailView(DetailView):
    title = "Movie detail view"
    template_name = "movies/movie_detail.html"
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return"] = self.request.META["HTTP_REFERER"]
        return context


class MovieModalView(DetailView):
    template_name = "movies/movie_modal.html"
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return"] = self.request.GET.get("return")
        return context
