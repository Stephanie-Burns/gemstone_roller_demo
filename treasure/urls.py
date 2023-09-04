from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gemstone/create/", views.gemstone_create, name="gemstone_create"),
    path("gemstone/all/", views.gemstone_all, name="gemstone_all")
]