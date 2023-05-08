from rest_framework import serializers

from follows.models import Follow

from books.models import Book
from books.serializers import BookSerializer

from users.models import User
from users.serializers import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField(
        method_name="get_book"
    )
    user = serializers.SerializerMethodField(
        method_name="get_user"
    )

    class Meta:
        model = Follow
        fields = ["id", "user", "book"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Follow:
        return Follow.objects.create(**validated_data)

    def get_book(self, obj: dict) -> Book:
        serializer = BookSerializer(obj.book)
        return serializer.data

    def get_user(self, obj: dict) -> User:
        serializer = UserSerializer(obj.user)
        return serializer.data
