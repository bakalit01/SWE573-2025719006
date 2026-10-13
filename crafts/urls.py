from django.urls import path

from . import views

app_name = "crafts"

urlpatterns = [
    path("", views.craft_list, name="list"),
    path("<slug:slug>/", views.craft_detail, name="detail"),
]
