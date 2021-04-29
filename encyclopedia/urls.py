from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("<str:name>", views.error, name="error")
]
