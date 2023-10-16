from django.urls import path

from .views import NoteListAPIView, NoteRetrieveDestroyAPIView, \
    TagListAPIView, NoteAPIView

urlpatterns = [
    path('notes', NoteAPIView.as_view()),
    path('tags', TagListAPIView.as_view()),
    # path('notes/<int:pk>', NoteRetrieveDestroyAPIView.as_view()),

]
