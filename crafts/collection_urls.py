from django.urls import path

from . import collection_views as views

app_name = "collections"

urlpatterns = [
    path("", views.saved, name="saved"),
    path("new/", views.collection_create, name="create"),
    path("<int:pk>/", views.collection_detail, name="detail"),
    path("<int:pk>/edit/", views.collection_edit, name="edit"),
    path("<int:pk>/delete/", views.collection_delete, name="delete"),
    path("<int:pk>/remove/<slug:slug>/", views.collection_remove, name="remove"),
]
