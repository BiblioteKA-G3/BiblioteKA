from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from books.models import Book
from books.serializers import BookSerializer

from users.permissions import IsAccountEmployee


class BookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateBookView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountEmployee]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RetriveBookView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAccountEmployee]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
