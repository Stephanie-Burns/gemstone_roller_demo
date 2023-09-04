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
    path("gemstone/all/", views.gemstone_all, name="gemstone_all"),
]