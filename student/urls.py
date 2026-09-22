from django.urls import path
from .views import (
    StudentListCreateView,
    StudentUpdateView,
    StudentDestroyView
)


urlpatterns = [
    path("student/",StudentListCreateView.as_view(),name="student-list-create"),
    path("student/<int:pk>/",StudentUpdateView.as_view(),name="student-update"),
    path("student/<int:pk>/delete/",StudentDestroyView.as_view(), name="student-delete"),
]

