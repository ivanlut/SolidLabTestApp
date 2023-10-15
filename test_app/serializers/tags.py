"""
Тут будут сериализаторы для запросов из views.tags
"""

from rest_framework import serializers

from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'