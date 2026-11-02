from django.urls import path

from . import review_views, story_views, views

app_name = "crafts"

urlpatterns = [
    path("", views.craft_list, name="list"),
    path("add/", views.craft_create, name="create"),
    path("mine/", views.my_crafts, name="mine"),
    path("fields/", views.attribute_fields, name="attribute_fields"),
    path("review/", review_views.review_queue, name="review_queue"),
    path("review/reports/<int:pk>/", review_views.handle_report, name="handle_report"),
    path("stories/<int:pk>/edit/", story_views.edit_story, name="edit_story"),
    path("stories/<int:pk>/delete/", story_views.delete_story, name="delete_story"),
    path("stories/<int:pk>/moderate/", story_views.moderate_story, name="moderate_story"),
    path("<slug:slug>/", views.craft_detail, name="detail"),
    path("<slug:slug>/edit/", views.craft_edit, name="edit"),
    path("<slug:slug>/delete/", views.craft_delete, name="delete"),
    path("<slug:slug>/review/", review_views.review_craft, name="review"),
    path("<slug:slug>/report/", review_views.report_craft, name="report"),
    path("<slug:slug>/stories/", story_views.add_story, name="add_story"),
]
