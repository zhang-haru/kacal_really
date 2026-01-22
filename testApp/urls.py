from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("timeline/", views.timeline, name="timeline"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("posts/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("signup/", views.signup, name="signup"),

    path("calorie/", views.calorie_dashboard, name="calorie_dashboard"),
    path("calorie/entries/", views.calorie_entry_list, name="calorie_entry_list"),
    path("calorie/entries/new/", views.calorie_entry_create, name="calorie_entry_create"),
    path("calorie/entries/<int:pk>/edit/", views.calorie_entry_update, name="calorie_entry_update"),
    path("calorie/entries/<int:pk>/delete/", views.calorie_entry_delete, name="calorie_entry_delete"),
    path("calorie/settings/", views.calorie_settings, name="calorie_settings"),
    path("calorie/copy-yesterday/", views.calorie_copy_yesterday, name="calorie_copy_yesterday"),
    path("calorie/export/", views.calorie_export_csv, name="calorie_export_csv"),
    path("calorie/api/entries/", views.calorie_api_entries, name="calorie_api_entries"),
]
