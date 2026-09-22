from django.urls import path
from .views import (
    AuthorListCreateView,
    AuthorUpdateView,
    AuthorDestroyView
)


urlpatterns = [
    path("author/",AuthorListCreateView.as_view(),name="author-list-create"),
    path("author/<int:pk>/",AuthorUpdateView.as_view(),name="author-update"),
    path("author/<int:pk>/delete/",AuthorDestroyView.as_view(),name="author-delete"),
]
