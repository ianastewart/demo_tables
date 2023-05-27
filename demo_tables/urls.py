from django.contrib import admin
from django.urls import path
from movies.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movies/", MoviesListView.as_view(), name="movies_list"),
    path("", MoviesTable1View.as_view(), name="table1"),
    path("table2/", MoviesTable2View.as_view(), name="table2"),
    path("table3/", MoviesTable3View.as_view(), name="table3"),
    path("table4/", MoviesTable4View.as_view(), name="table4"),
    path("table5/", MoviesTable5View.as_view(), name="table5"),
    path("table6/", MoviesTable6View.as_view(), name="table6"),
]
