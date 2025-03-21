
from django.urls import path

from . import views


app_name = "treasure"

urlpatterns = [
    path("", views.index, name="index"),
    path("gemstone/", views.gemstone_index, name="gemstone_index"),
    path("gemstone/create/", views.gemstone_create, name="gemstone_create"),
    path("gemstone/view/<int:gemstone_id>/", views.gemstone_view, name="gemstone_view"),
    path("gemstone/edit/<int:gemstone_id>/", views.gemstone_edit, name="gemstone_edit"),
    path("gemstone/delete/<int:gemstone_id>/", views.gemstone_delete, name="gemstone_delete"),
    path("gemstone/search/", views.gemstone_search, name="gemstone_search"),
    path("gemstone/roll/", views.gemstone_roll, name="gemstone_roll"),

    # HTMX Endpoints
    path("gemstone/search-table/", views.gemstone_search_table, name="gemstone_search_table"),
    path("gemstone/form/", views.gemstone_form, name="gemstone_form"),

    # Deprecated Endpoints
    # path("gemstone/all/", views.gemstone_all, name="gemstone_all"),
]