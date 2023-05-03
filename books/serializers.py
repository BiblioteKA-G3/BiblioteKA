from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    title = serializers.EmailField(
        max_length=200,
        validators=[UniqueValidator(queryset=Book.objects.all())],
    )

    class Meta:
        model = Book
        fields = ["id", "title", "author", "pages", "publisher", "release_date"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Book:
        return Book.objects.create(**validated_data)
