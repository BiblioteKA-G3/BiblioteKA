from copies.models import Copy

from books.models import Book
from books.serializers import BookSerializer

from rest_framework import serializers


class CopySerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField(
        method_name="get_book"
    )

    class Meta:
        model = Copy
        fields = ["id", "copy_count", "book"]
        read_only_fields = ["id", "book"]

    def create(self, validated_data: dict) -> Copy:
        return Copy.objects.create(**validated_data)

    def get_book(self, obj: Copy) -> dict:
        book = Book.objects.get(id=obj.book_id)
        serializer = BookSerializer(book)

        return serializer.data
