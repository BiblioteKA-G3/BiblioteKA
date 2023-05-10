from rest_framework.generics import (
    CreateAPIView,
    ListAPIView
)
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from books.models import Book
from copies.models import Copy
from copies.serializers import CopySerializer


class CreateCopyView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs.get("id"))

        if Copy.objects.filter(book_id=book).exists():
            raise ValidationError({"Error Message": "Book Already exists"})

        serializer.save(book=book)


class ListCopies(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
