from django.urls import path
from .views import (
    BookIssueListCreateView,
    BookIssueUpdateView,
    BookIssueDestroyView
)


urlpatterns = [
    path("bookissue/",BookIssueListCreateView.as_view(),name="book-list-create" ),
    path("bookissue/<int:pk>/",BookIssueUpdateView.as_view(),name="book-update"),
    path("bookissue/<int:pk>/delete/",BookIssueDestroyView.as_view(),name="book-delete"),
]
