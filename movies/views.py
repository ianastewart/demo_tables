from django.shortcuts import render, reverse

from django.views.generic import ListView, TemplateView
from django_htmx.http import HttpResponseClientRedirect
from .models import Movie
from tables_pro.views import TablesProView
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
            ("action_page", "Page action"),
            ("export", "Export"),
        )

    def handle_action(self, request):
        if "action" in request.POST:
            # do something
            return None
        elif "action_modal" in request.POST:
            context = {"selected": self.selected_objects}
            return render(request, "movies/action_modal.html", context)
        elif "action_page" in request.POST:
            request.session["selected_ids"] = self.selected_ids
            return HttpResponseClientRedirect(reverse("action_page"))


class ActionPageView(TemplateView):
    template_name = "movies/action_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.filter(
            id__in=self.request.session.get("selected_ids", [])
        )
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


class MoviesTable6View(TablesProView):
    title = "Filter toolbar"
    table_class = MovieTable1
    filterset_class = MovieFilter
    filter_style = TablesProView.FilterStyle.MODAL
    template_name = "movies/table.html"
    model = Movie
