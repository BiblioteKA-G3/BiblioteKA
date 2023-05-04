from django.urls import path
from . import views


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/create/", views.CreateBookView.as_view()),
    path("books/<int:pk>/", views.RetriveBookView.as_view()),
]
