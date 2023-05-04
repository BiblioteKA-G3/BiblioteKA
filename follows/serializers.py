from rest_framework import serializers
from follows.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "user_id", "book_id"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> Follow:
        return Follow.objects.create(**validated_data)
