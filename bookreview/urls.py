from django.urls import path
from .views import (
    BookReviewListCreateView,
    BookReviewUpdateView,
    BookReviewDestroyView
)


urlpatterns = [
    path("bookreview/",BookReviewListCreateView.as_view(),name="book-list-create" ),
    path("bookreview/<int:pk>/",BookReviewUpdateView.as_view(),name="book-update"),
    path("bookreview/<int:pk>/delete/",BookReviewDestroyView.as_view(),name="book-delete"),
]
