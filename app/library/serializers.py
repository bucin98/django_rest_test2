from rest_framework import serializers
from .models import Author, Book, Genres


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title')


class AuthorFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookFullSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True,
        queryset=Author.objects.all(),
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
