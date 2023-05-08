from rest_framework import serializers
from rest_framework.serializers import ValidationError
from loans.models import Loan
import datetime


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "loan_date", "return_date", "user", "copy"]
        read_only_fields = ["id", "loan_date", "return_date"]

    def get_return_date(self, loan_date):
        exclude_days = [5, 6]
        days_count = 0

        while days_count < 7:
            loan_date += datetime.timedelta(days=1)
            if loan_date.weekday() not in exclude_days:
                days_count += 1
        return loan_date

    def create(self, validated_data: dict) -> Loan:
        loan_date = validated_data["loan_date"]
        return_date = self.get_return_date(loan_date)

        validated_data["return_date"] = return_date

        return Loan.objects.create(**validated_data)
