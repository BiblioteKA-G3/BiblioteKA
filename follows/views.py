from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.views import status, Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from follows.models import Follow
from follows.serializers import FollowSerializer

from books.models import Book
from users.models import User


# Create your views here.
class FollowsCreateDestroyView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        if Follow.objects.filter(user_id=user).exists():
            raise ValidationError({"Error Message": "Follow already exists"})

        serializer.save(user=user, book=book)

    def destroy(self, request, *args, **kwargs):
        book = Book.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        relation = Follow.objects.filter(user_id=user, book_id=book)
        if not relation:
            raise ValidationError(
                {"Error Message": "Relation does not exists"}
            )

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
