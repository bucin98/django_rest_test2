from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Author, Book, Genres
from .serializers import AuthorFullSerializer, BookFullSerializer, AuthorListSerializer, BookListSerializer, \
    GenreSerializer
from .utils import is_valid_uuid


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorFullSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorListSerializer
        return AuthorFullSerializer

    def delete(self, request, *args, **kwargs):
        author_id = request.data.get('author_id')
        if is_valid_uuid(author_id):
            author = get_object_or_404(Author, pk=author_id)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid author_id format"})


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorFullSerializer


class BookList(generics.ListCreateAPIView):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookFullSerializer

    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')
        book_name = self.request.query_params.get('book_name')

        if book_name:
            queryset = queryset.filter(title__icontains=book_name)

        return queryset

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        if is_valid_uuid(book_id):
            book = get_object_or_404(Book, pk=book_id)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid book_id format"})


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookFullSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genres.objects.all().order_by('name')
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
