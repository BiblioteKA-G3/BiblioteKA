from django.urls import path
from . import views


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int: id>/", views.RetriveBookView.as_view()),
]
