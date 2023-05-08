from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
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

from copies.models import Copy


class LoanView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanDetailView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def post(self, request: Request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        copy = get_object_or_404(Copy, id=kwargs.get("pk"))

        relation = Loan.objects.filter(user_id=user, copy_id=copy)
        if relation:
            raise ValidationError({"Error Message": "Relation already exists"})

        loan_data = {
            "user": user.id,
            "copy": copy.id,
            "loan_date": datetime.date.today(),
        }
        serializer = self.get_serializer(data=loan_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(loan_date=datetime.date.today())

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs):
        loan = self.get_object()
        user = loan.user

        if loan.return_date < timezone.now().date():
            user.loan_status = False
            user.save()

        if user.loan_status is False:
            return Response({"Error Message": "User cannot borrow a book"})

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        copy = Copy.objects.get(id=self.kwargs.get("pk"))
        user = User.objects.get(id=self.request.user.id)

        relation = Loan.objects.filter(user_id=user, copy_id=copy)
        if not relation:
            raise ValidationError({"Error Message": "Loan does not exists"})

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
