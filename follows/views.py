from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.views import status, Response
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from follows.models import Follow
from follows.serializers import FollowSerializer

from books.models import Book

from users.models import User

from copies.models import Copy


class FollowsCreateDestroyView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs.get("pk"))
        user = request.user

        copy = get_object_or_404(Copy, book_id=book.id)

        if copy.copy_count == 0:
            followers = Follow.objects.filter(book=book).values_list(
                "user__email", flat=True
            )

            subject = f"{book.title} it is unavailable now"
            message = f"The Book {book.title} of {book.author} Not Available."
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers,
                fail_silently=False,
            )
            return Response(
                {"Message": "This book has no copies"}, status.HTTP_400_BAD_REQUEST
            )

        user.follows_books.add(book)
        user.save()

        return Response(
            {"Message": f"Now you're following: {book.title}"}, status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        book = Book.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        relation = Follow.objects.filter(user_id=user, book_id=book)
        if not relation:
            raise ValidationError({"Error Message": "Follow does not exists"})

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
