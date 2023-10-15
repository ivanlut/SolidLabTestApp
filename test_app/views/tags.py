from rest_framework.generics import ListAPIView, CreateAPIView

from ..models import Tag
from ..serializers import TagSerializer


class TagListAPIView(ListAPIView, CreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
