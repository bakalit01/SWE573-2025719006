from django.urls import path

from . import review_views, views

app_name = "crafts"

urlpatterns = [
    path("", views.craft_list, name="list"),
    path("add/", views.craft_create, name="create"),
    path("mine/", views.my_crafts, name="mine"),
    path("fields/", views.attribute_fields, name="attribute_fields"),
    path("review/", review_views.review_queue, name="review_queue"),
    path("review/reports/<int:pk>/", review_views.handle_report, name="handle_report"),
    path("<slug:slug>/", views.craft_detail, name="detail"),
    path("<slug:slug>/edit/", views.craft_edit, name="edit"),
    path("<slug:slug>/delete/", views.craft_delete, name="delete"),
    path("<slug:slug>/review/", review_views.review_craft, name="review"),
    path("<slug:slug>/report/", review_views.report_craft, name="report"),
]
