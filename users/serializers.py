from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "cpf",
            "birthdate",
            "loan_status",
            "student",
            "blocked_date",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="user with this username already exists.",
                    )
                ]
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all()
                    )
                ]
            },
            "cpf": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="user with this cpf already exists.",
                    )
                ]
            },
        }

    def create(self, validated_data: dict) -> User:
        if validated_data["student"] is True:
            return User.objects.create_user(**validated_data)
        else:
            return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance
