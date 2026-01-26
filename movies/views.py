from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import ListView, TemplateView, DetailView
from django_htmx.http import (
    HttpResponseClientRedirect,
    retarget, trigger_client_event,
)
from django_tableaux.views import TableauxView, SelectedMixin
from django_tableaux.models import Pagination, FilterStyle, ClickAction
from .filters import MovieFilter
from .forms import MovieForm, BasicSettingsForm
from .models import Movie
from .tables import MovieTable, MovieTableSelection, MovieTableResponsive, MovieTable4

class PlayView(TemplateView):
    template_name = "movies/play.html"

class TableauxInteractiveView(TableauxView):
    # Inherit the standard TableauxView and override setup so it reads parameters
    # from the session to support the interactive demo.

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if "TABLEAUX_SETTINGS" in request.session.keys():
            settings = request.session["TABLEAUX_SETTINGS"]
            for k, v in settings.items():
                if isinstance(v, bool):
                    self.__setattr__(k, v)
                elif k == "pagination":
                    self.pagination = Pagination(v)
                elif k == "filter_style":
                    self.filter_style = FilterStyle(v)
                elif k == "click_action":
                    self.clickaction = ClickAction(v)
                elif k == "fixed_height":
                    self.fixed_height = int(v)
        pass


class InteractiveView(TemplateView):
    title = "Interactive tableaux view"
    template_name = "movies/interactive.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        initial = {}
        if self.request.session.get("TABLEAUX_SETTINGS"):
            initial=self.request.session["TABLEAUX_SETTINGS"]
        context["form"] = BasicSettingsForm(initial=initial)
        context["url_name"] = "filter_toolbar"
        return context

    def post(self, request, *args, **kwargs):
        form = BasicSettingsForm(request.POST)
        if form.is_valid():
            self.request.session["TABLEAUX_SETTINGS"] = {}
            for k, v in form.cleaned_data.items():
                self.request.session["TABLEAUX_SETTINGS"][k] = v
            self.request.session.modified=True
        response = HttpResponse()
        return trigger_client_event(response, name="reloadTableaux")


class BasicInteractiveView(TableauxInteractiveView):
    title = "Basic table interactive"
    caption = "This table has a caption"
    table_class = MovieTable
    model = Movie


class BasicView(TableauxView):
    title = "Basic table"
    caption = "This table has a caption"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    update_url = False
    # pagination = Pagination.PAGED

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class BasicViewNew(TemplateView):
    title = "Basic view new"
    template_name = "movies/table_component.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        initial = {}
        if self.request.session["TABLEAUX_SETTINGS"]:
            initial=self.request.session["TABLEAUX_SETTINGS"]
        context["form"] = BasicSettingsForm(initial=initial)
        return context

    def post(self, request, *args, **kwargs):
        form = BasicSettingsForm(request.POST)
        if form.is_valid():
            self.request.session["TABLEAUX_SETTINGS"] = {}
            for k, v in form.cleaned_data.items():
                self.request.session["TABLEAUX_SETTINGS"][k] = v
            self.request.session.modified=True
        response = HttpResponse()
        return trigger_client_event(response, name="reloadTableaux")



class RowColSettingsView(TableauxView):
    title = "Row and column settings"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    row_settings = True
    column_settings = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["css_toolbar"] = "bg-light"
        context["css_table"] = "bg-white"
        return context


class SelectActionsView(TableauxInteractiveView):
    title = "Selection and actions"
    table_class = MovieTableSelection
    template_name = "movies/table.html"
    model = Movie
    prefix = "X"

    def get_bulk_actions(self):
        return (
            ("action_modal", "Action in a modal"),
            ("action_page", "Action on a new page"),
            ("export", "Export to csv"),
            ("export_xlsx", "Export as xlsx"),
        )

    def handle_action(self, request, action):
        if action == "action_modal":
            context = {"selected": self.selected_objects}
            return render(request, "movies/action_modal.html", context)

        elif action == "action_page":
            request.session["selected_ids"] = self.selected_ids
            request.session["return_url"] = self.return_url
            path = reverse("action_page")
            return HttpResponseClientRedirect(path)
        raise ValueError(f"Django tableaux: action {action} has no handler")

class ActionPageView(SelectedMixin, TemplateView):
    model = Movie
    filterset_class = MovieFilter
    template_name = "movies/action_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = self.get_query_set()
        context["return_url"] = self.return_url
        return context


class InfiniteScrollView(TableauxView):
    title = "Infinite scroll with sticky header in fixed height of 500px"
    table_class = MovieTableSelection
    template_name = "movies/table.html"
    model = Movie
    column_settings = True
    row_settings = True
    infinite_scroll = True
    sticky_header = True
    fixed_height = 500
    indicator = True

    def get_bulk_actions(self):
        return (("action_message", "Action with message"),)


class InfiniteLoadView(TableauxView):
    title = "Infinite load more"
    table_class = MovieTable
    template_name = "movies/table.html"
    model = Movie
    infinite_load = True
    sticky_header = True


class ResponsiveView(SelectActionsView):
    title = "Responsive"
    table_class = MovieTableResponsive
    column_settings = True
    infinite_load = True


class ResponsiveComponentView(TableauxView):
    table_class = MovieTableResponsive
    template_name = "movies/table_component.html"
    model = Movie


class MoviesFilterToolbarView(SelectActionsView):
    title = "Filter toolbar"
    table_class = MovieTableResponsive
    filterset_class = MovieFilter
    model = Movie
    filter_style = FilterStyle.TOOLBAR
    column_settings = True
    row_settings = True
    responsive = True
    update_url = False
    filter_button = False
    filter_pills = False



class MoviesFilterModalView(SelectActionsView):
    title = "Filter modal"
    table_class = MovieTableResponsive
    filterset_class = MovieFilter
    filter_style = FilterStyle.MODAL
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    model = Movie
    filter_button = False
    filter_pills = True
    prefix="X"
    update_url = False


class MoviesFilterHeaderView(SelectActionsView):
    title = "Filter in header"
    table_class = MovieTableResponsive
    filterset_class = MovieFilter
    filter_style = FilterStyle.HEADER
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    sticky_header = True
    fixed_height = 300
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
    click_action = ClickAction.GET
    click_url_name = "movie_detail"


class MoviesRowClickModalView(TableauxView):
    title = "Click row shows detail modal "
    template_name = "movies/table.html"
    table_class = MovieTable
    model = Movie
    click_action = ClickAction.HX_GET
    click_url_name = "movie_modal"


class MoviesRowClickCustomView(TableauxView):
    title = "Custom click cell"
    template_name = "movies/table.html"
    table_class = MovieTableResponsive
    model = Movie
    click_action = ClickAction.CUSTOM

    def cell_clicked(self, pk, column_name, target):
        movie = Movie.objects.get(pk=pk)
        context = {
            "message": f"'{movie.title}', primary key: {pk}, column: {column_name} was clicked.",
            "alert_class": "alert-info",
        }
        response = render(self.request, "movies/message.html", context)
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
