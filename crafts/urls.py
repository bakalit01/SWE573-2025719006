from django.urls import path

from . import views

app_name = "crafts"

urlpatterns = [
    path("", views.craft_list, name="list"),
    path("add/", views.craft_create, name="create"),
    path("mine/", views.my_crafts, name="mine"),
    path("fields/", views.attribute_fields, name="attribute_fields"),
    path("<slug:slug>/", views.craft_detail, name="detail"),
    path("<slug:slug>/edit/", views.craft_edit, name="edit"),
    path("<slug:slug>/delete/", views.craft_delete, name="delete"),
]
