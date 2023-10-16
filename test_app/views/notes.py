from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from ..models import Note
from ..serializers import NoteSerializer


class NoteListAPIView(ListAPIView, CreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.select_related('content').prefetch_related(
        'tags').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['content__text']


class NoteAPIView(APIView):

    @staticmethod
    def get(request):
        query_id = request.query_params.get('id', None)
        if query_id:
            note = get_object_or_404(Note.objects.select_related('content'),
                                     pk=query_id)
            serializer = NoteSerializer(note)
            return Response(serializer.data, status.HTTP_200_OK)

        query = request.query_params.get('query', None)
        db_query = Note.objects.select_related(
            'content').prefetch_related('tags')
        if query:
            db_query = db_query.filter(content__text__contains=query)
        serializer = NoteSerializer(db_query.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        query_id = request.query_params.get('id', None)
        note = get_object_or_404(Note, pk=query_id)
        note.delete()
        return Response({"id": int(query_id)}, status=status.HTTP_200_OK)


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

