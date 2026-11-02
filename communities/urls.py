from django.urls import path

from . import views

app_name = "communities"

urlpatterns = [
    path("<str:slug>/", views.community_detail, name="detail"),
    path("<str:slug>/edit/", views.community_edit, name="edit"),
]
