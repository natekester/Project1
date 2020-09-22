from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.make_entry, name="make_entry"),
    path("wiki/<str:name>", views.get_entry, name="get_entry")
    

]
