from django.urls import path
from books.views import (
    BookView,
    CreateBookView,
    RetriveBookView
)


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/create/", CreateBookView.as_view()),
    path("books/<int:pk>/", RetriveBookView.as_view()),
]
