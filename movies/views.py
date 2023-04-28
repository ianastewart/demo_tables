from django.shortcuts import render

from django.views.generic import ListView
from .models import Movie
from tables_pro.views import TablesProView
from .tables import MovieTable1, MovieTable3


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
        return (("action_1", "Action number 1"), ("action_2", "Action number 2"))
