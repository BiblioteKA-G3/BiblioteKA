from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status, Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings
from follows.models import Follow
from follows.serializers import FollowSerializer

from books.models import Book
from users.models import User

from django.core.mail import send_mail


# Create your views here.
class FollowsCreateDestroyView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        # if Follow.objects.filter(user_id=user).exists():
        #     raise ValidationError({"Error Message": "Follow already exists"})

        if book.copies.copy_count > 0:
            raise ValidationError({"Error Message": "Book is already available"})

        if book.copies.copy_count == 0:
            followers = Follow.objects.filter(book=book).values_list(
                "user__email", flat=True
            )
            subject = (f"{book.title} esta indisponivel agora",)
            message = f"O livro {book.title} de {book.author} agora não disponível."
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                followers,
                fail_silently=False,
            )

        serializer.save(user=user, book=book)

    def destroy(self, request, *args, **kwargs):
        book = Book.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        relation = Follow.objects.filter(user_id=user, book_id=book)
        if not relation:
            raise ValidationError({"Error Message": "Relation does not exists"})

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
