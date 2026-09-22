from django.urls import path
from .views import (
    BookListCreateView,
    BookUpdateView,
    BookDestroyView
)


urlpatterns = [
    path("book/",BookListCreateView.as_view(),name="book-list-create" ),
    path("book/<int:pk>/",BookUpdateView.as_view(),name="book-update"),
    path("book/<int:pk>/delete/",BookDestroyView.as_view(),name="book-delete"),
]
