from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, filters

from ..models import Note
from ..serializers import NoteSerializer


class NoteListAPIView(ListAPIView, CreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.select_related('content').prefetch_related(
        'tags').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['content__text']


class NoteRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.select_related('content').prefetch_related(
        'tags').all()
    http_method_names = ['get', 'delete']


    # если не переопределить вернется 204 без body при удаление
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"id": kwargs['pk']}, status=status.HTTP_200_OK)

