from django.db import models
import uuid


class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    title = models.CharField(max_length=100)
    genre = models.ForeignKey('Genres', on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title


class Genres(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
