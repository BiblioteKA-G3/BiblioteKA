from rest_framework.generics import (
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import Request, Response, status
from rest_framework.exceptions import ValidationError

import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from loans.models import Loan
from loans.serializers import LoanSerializer

from users.models import User

from books.models import Book

from copies.models import Copy

from follows.models import Follow

from django.conf import settings
from django.core.mail import send_mail


class LoanView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


# class LoanHistoryStudentView(RetrieveAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer


class LoanDetailView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def post(self, request: Request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        copy = get_object_or_404(Copy, id=kwargs.get("pk"))

        # import ipdb

        # ipdb.set_trace()

        if copy.copy_count == 0:
            raise ValidationError({"Error Message": "Not copy"})

        blocked_date = user.blocked_date
        if blocked_date is not None:
            if blocked_date > datetime.date.today():
                raise ValidationError({"Error Message": "You are still blocked"})

        copy.copy_count = copy.copy_count - 1
        copy.save()

        relation = Loan.objects.filter(user_id=user, copy_id=copy)
        if relation:
            raise ValidationError({"Error Message": "Loan already exists"})

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

        relation = Loan.objects.filter(user_id=user, copy_id=copy)
        if not relation:
            raise ValidationError({"Error Message": "Loan does not exists"})

        copy.copy_count = copy.copy_count + 1
        copy.save()

        send_mail(
            subject=f"{book.title} ja disponivel",
            message=f"The Book {book.title} of {book.author} Available.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=followers,
            fail_silently=False,
        )

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
