from django.contrib import admin
from django.urls import path
from movies.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("play/", PlayView.as_view(), name="play"),
    path("interactive/", InteractiveView.as_view(), name="interactive"),
    path("tableaux/basic/", BasicInteractiveView.as_view(), name="basic_interactive"),
    path("", BasicView.as_view(), name="basic"),
    path("new/", BasicViewNew.as_view(), name="basic-new"),
    path("rowcol/", RowColSettingsView.as_view(), name="row_col"),
    path("select/", SelectActionsView.as_view(), name="select_actions"),
    path("inf_scroll/", InfiniteScrollView.as_view(), name="infinite_scroll"),
    path("inf_load/", InfiniteLoadView.as_view(), name="infinite_load"),
    path("responsive/", ResponsiveView.as_view(), name="responsive"),
    path("responsive/component/", ResponsiveComponentView.as_view(), name="responsive-component"),
    path("filter_t/", MoviesFilterToolbarView.as_view(), name="filter_toolbar"),
    path("filter_m/", MoviesFilterModalView.as_view(), name="filter_modal"),
    path("filter_h/", MoviesFilterHeaderView.as_view(), name="filter_header"),
    path("editable/", MoviesEditableView.as_view(), name="editable"),
    path("row_click/", MoviesRowClickView.as_view(), name="row_click"),
    path("row_click_modal/", MoviesRowClickModalView.as_view(), name="row_click_modal"),
    path(
        "row_click_custom/", MoviesRowClickCustomView.as_view(), name="row_click_custom"
    ),
    path("action/", ActionPageView.as_view(), name="action_page"),
    path("detail/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("modal/<int:pk>/", MovieModalView.as_view(), name="movie_modal"),
]
