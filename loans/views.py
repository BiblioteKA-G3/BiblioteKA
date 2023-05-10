from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import (
    Request,
    Response,
    status
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from loans.models import Loan
from users.models import User
from books.models import Book
from copies.models import Copy
from follows.models import Follow

from loans.serializers import LoanSerializer

import datetime


class LoanView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanHistoryStudentView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer

    def get_queryset(self):
        loans = Loan.objects.filter(
            user=self.kwargs.get("pk")
        )

        return loans


class LoanDetailView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def post(self, request: Request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        copy = get_object_or_404(Copy, id=kwargs.get("pk"))

        if copy.copy_count == 0:
            raise ValidationError(
                {"Error Message": "This book has no copies available"}
            )

        blocked_date = user.blocked_date
        if blocked_date is not None:
            if blocked_date > datetime.date.today():
                raise ValidationError(
                    {"Error Message": "User still blocked"}
                )

        copy.copy_count = copy.copy_count - 1
        copy.save()

        relation = Loan.objects.filter(user_id=user, copy_id=copy)
        if relation:
            raise ValidationError(
                {"Error Message": "This Loan already exists."}
            )

        loan_data = {
            "user": user.id,
            "copy": copy.id,
            "loan_date": datetime.date.today(),
        }
        serializer = self.get_serializer(data=loan_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(loan_date=datetime.date.today(), user=user, copy=copy)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        copy = Copy.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)
        book = Book.objects.get(id=copy.book_id)

        followers = Follow.objects.filter(book=book).values_list(
            "user__email", flat=True
        )

        relation = Loan.objects.filter(user_id=user.id, copy_id=copy.id)

        if not relation:
            raise ValidationError(
                {"Error Message": "Loan doesn't exists."}
            )

        copy.copy_count = copy.copy_count + 1
        copy.save()

        send_mail(
            subject=f"{book.title} is available.",
            message=f"The Book {book.title} of {book.author} is available to loan.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=followers,
            fail_silently=False,
        )

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
