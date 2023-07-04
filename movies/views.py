from django.shortcuts import render, reverse
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django_htmx.http import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
    retarget,
)
from django.http import HttpResponse
from .models import Movie
from .forms import MovieForm
from tables_pro.views import TablesProView, SelectedMixin
from .tables import MovieTable1, MovieTable2, MovieTable3, MovieTable4
from .filters import MovieFilter
from django.utils.safestring import mark_safe


class MoviesListView(ListView):
    model = Movie
    template_name = "movies/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movies"] = Movie.objects.all().order_by("title")
        return context


class BasicView(TablesProView):
    title = "Basic view"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie


class RowColSettingsView(TablesProView):
    title = "Row and column settings"
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


class SelectActionsView(TablesProView):
    title = "Selection and actions"
    table_class = MovieTable2
    template_name = "movies/table.html"
    model = Movie

    def get_actions(self):
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
            response = render(request, "tables_pro/_alert.html", context)
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


class InfiniteScollView(TablesProView):
    title = "Infinite scroll"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie
    infinite_scroll = True
    sticky_header = True


class InfiniteLoadView(TablesProView):
    title = "Infinite load more"
    table_class = MovieTable1
    template_name = "movies/table.html"
    model = Movie
    infinite_load = True
    sticky_header = True


class MoviesFilterToolbarView(SelectActionsView):
    title = "Filter toolbar"
    table_class = MovieTable3
    filterset_class = MovieFilter
    filter_style = TablesProView.FilterStyle.TOOLBAR
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    model = Movie


class MoviesFilterModalView(SelectActionsView):
    title = "Filter modal"
    table_class = MovieTable3
    filterset_class = MovieFilter
    filter_style = TablesProView.FilterStyle.MODAL
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    model = Movie


class MoviesFilterHeaderView(SelectActionsView):
    title = "Filter in header"
    table_class = MovieTable3
    filterset_class = MovieFilter
    filter_style = TablesProView.FilterStyle.HEADER
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True
    responsive = True
    sticky_header = True
    infinite_scroll = True


class MoviesEditableView(TablesProView):
    title = "Editable columns"
    model = Movie
    table_class = MovieTable4
    template_name = "movies/table.html"
    column_settings = True
    row_settings = True

    def cell_clicked(self, record_pk, column_name, target):
        form = MovieForm()
        context = {"field": form.fields["vote"]}
        s = render(self.request, "tables_pro/cell_form.html", context)
        return s

        # str = f"<input name='vote' id='target' hx-post='' hx-target='#{target}' on_change=doHxPost>"
        # return HttpResponse(mark_safe(str))

    def cell_changed(self, record_pk, column_name, target):
        movie = Movie.objects.get(pk=record_pk)
        movie.column_name = "9999"
        movie.save()
        return HttpResponseClientRefresh
