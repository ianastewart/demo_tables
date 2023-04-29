from django.contrib import admin
from django.urls import path
from movies.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movies/", MoviesListView.as_view(), name="movies_list"),
    path("table1/", MoviesTable1View.as_view(), name="table1"),
    path("table2/", MoviesTable2View.as_view(), name="table2"),
    path("table3/", MoviesTable3View.as_view(), name="table3"),
]
