"""
Тут будут сериализаторы для запросов из views.notes
"""

from rest_framework import serializers

from ..models import Note, Content, Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(source='content.text')
    tags_ids = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False, write_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = 'id', 'title', 'content', 'tags', 'tags_ids'

    def create(self, validated_data):
        content = validated_data.pop('content', None)
        tags_ids = validated_data.pop('tags_ids', [])
        content = Content.objects.create(text=content['text'])
        validated_data['content_id'] = content.id
        note = super().create(validated_data)
        if len(tags_ids) > 0:
            note.tags.add(*tags_ids)
        return note

