from rest_framework import serializers
from copies.models import Copy


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "copy_count", "book_id"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Copy:
        return Copy.objects.create(**validated_data)
