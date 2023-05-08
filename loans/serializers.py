from rest_framework import serializers
from rest_framework.serializers import ValidationError

from datetime import timedelta, date

from loans.models import Loan

from users.models import User
from users.serializers import UserSerializer

from copies.models import Copy
from copies.serializers import CopySerializer


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user")

    copy = serializers.SerializerMethodField(method_name="get_copy")

    class Meta:
        model = Loan
        fields = ["id", "loan_date", "return_date", "copy", "user"]
        read_only_fields = [
            "id",
            "loan_date",
            "return_date",
        ]

    def get_return_date(self, loan_date):
        exclude_days = [5, 6]
        days_count = 0

        while days_count < 7:
            loan_date += timedelta(days=1)
            if loan_date.weekday() not in exclude_days:
                days_count += 1
        return loan_date

    def create(self, validated_data: dict) -> Loan:
        loan_date = validated_data["loan_date"] - timedelta(days=1)
        return_date = self.get_return_date(loan_date)

        validated_data["return_date"] = return_date

        # import ipdb

        # ipdb.set_trace()

        user = validated_data["user"]
        if validated_data["user"].loans.filter(return_date__lt=date.today()):
            user.loan_status = False
            user.blocked_date = date.today() + timedelta(days=3)
            user.save()
            raise ValidationError({"Error Message": "User cannot borrow a book"})

        return Loan.objects.create(**validated_data)

    def get_user(self, obj: Loan) -> dict:
        user = User.objects.get(id=obj.user_id)
        serializer = UserSerializer(user)

        return serializer.data

    def get_copy(self, obj: Loan) -> dict:
        copy = Copy.objects.get(id=obj.copy_id)
        serializer = CopySerializer(copy)

        return serializer.data
