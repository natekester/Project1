from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.make_entry, name="make_entry"),
    path("wiki/<str:name>", views.get_entry, name="get_entry"),
    path("random", views.random_entry, name="random_entry"),
    path("search_redirect", views.search_redirect, name="search_redirect"),
    path("edit_redirect/<str:name>", views.edit_redirect, name="edit_redirect"),
    path("search/<str:search>", views.search, name="search"),
    path("edit/<str:wiki_name>", views.edit, name="edit")

]
