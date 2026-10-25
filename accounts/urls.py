from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("makers/<int:pk>/", views.profile, name="profile"),
    path("accounts/profile/edit/", views.edit_profile, name="edit_profile"),
]
