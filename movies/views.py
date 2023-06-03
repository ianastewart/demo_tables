from django.shortcuts import render, reverse

from django.views.generic import ListView, TemplateView
from django_htmx.http import HttpResponseClientRedirect
from .models import Movie
from tables_pro.views import TablesProView, SelectedMixin
from .tables import MovieTable1, MovieTable3
from .filters import MovieFilter


class MoviesListView(ListView):
    model = Movie
    template_name = "movies/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.all().order_by("title")
        return context


class MoviesTable1View(TablesProView):
    title = "Basic view"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie


class MoviesTable2View(TablesProView):
    title = "Row and column setting"
    table_class = MovieTable1
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


class MoviesTable3View(TablesProView):
    title = "Selection and actions"
    table_class = MovieTable3
    template_name = "movies/table.html"
    model = Movie

    def get_actions(self):
        return (
            ("action", "Invisible action"),
            ("action_modal", "Modal action"),
            ("action_page", "Action on a new page"),
            ("export", "Export"),
        )

    def handle_action(self, request, action):
        if action == "action":
            # do something
            return None
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


class MoviesTable4View(TablesProView):
    title = "Infinite scroll"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie
    infinite_scroll = True
    sticky_header = True


class MoviesTable5View(TablesProView):
    title = "Infinite load more"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie
    infinite_load = True
    sticky_header = True


class MoviesTable6View(MoviesTable3View):
    title = "Filter toolbar"
    table_class = MovieTable3
    filterset_class = MovieFilter
    filter_style = TablesProView.FilterStyle.MODAL
    template_name = "movies/table.html"
    model = Movie
