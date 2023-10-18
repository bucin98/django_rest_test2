import pytest
from rest_framework.test import APIClient
from .models import Book, Author, Genres
from django.urls import reverse


@pytest.mark.django_db
def test_author_creation():
    client = APIClient()
    names = ['Andx', 'Blqwe', 'casqwe', 'dqweq']
    url = reverse('author-list')
    num = 0
    for name in names:
        response = client.post(url, {'name': name})
        num += 1
        assert response.status_code == 201
        assert num == Author.objects.count()
        assert name == Author.objects.order_by().last().name


@pytest.mark.django_db
def test_author_list():
    client = APIClient()
    names = ['Andx', 'Blqwe', 'casqwe', 'dqweq']

    [Author.objects.create(name=x) for x in names]

    url = reverse('author-list')
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert all(data['results'][i]['name'] == names[i] for i in range(len(names)))


@pytest.mark.django_db
def test_author_update():
    client = APIClient()
    obj = Author.objects.create(name='one')
    url = reverse('author-detail', kwargs={'pk': obj.id})
    response = client.put(url, {'name': 'two'})
    obj_new = Author.objects.first()
    assert response.status_code == 200
    assert obj_new.name == 'two'


@pytest.mark.django_db
def test_author_delete():
    client = APIClient()
    obj = Author.objects.create(name='pao')
    all_object = Author.objects.count()
    assert 1 == all_object

    url = reverse('author-list')
    response = client.delete(url, data={'author_id': obj.id})
    assert response.status_code == 204

    all_object = Author.objects.count()
    assert 0 == all_object


@pytest.mark.django_db
def test_book_creation():
    client = APIClient()
    authors = [Author.objects.create(name='Author1'), Author.objects.create(name='Author2')]
    genre = Genres.objects.create(name='Fiction')
    url = reverse('book-list')

    response = client.post(url, {
        'title': 'Book1',
        'genre': genre.name,
        'authors': [authors[0].name, authors[1].name]
    })

    assert response.status_code == 201
    assert Book.objects.count() == 1
    book = Book.objects.first()
    assert book.title == 'Book1'
    assert book.genre == genre
    assert list(book.authors.all()) == authors


@pytest.mark.django_db
def test_book_list():
    client = APIClient()
    authors = [Author.objects.create(name='Author1'), Author.objects.create(name='Author2')]
    genre = Genres.objects.create(name='Fiction')
    books = [Book.objects.create(title=f'Book{i}', genre=genre) for i in range(1, 6)]
    for book, author in zip(books, authors):
        book.authors.add(author)

    url = reverse('book-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()

    assert len(data['results']) == 5
    for i, book in enumerate(books):
        assert data['results'][i]['title'] == f'Book{i + 1}'

    response = client.get(url, data={'book_name': 'Book'})
    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 5

    response = client.get(url, data={'book_name': '1'})
    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 1


@pytest.mark.django_db
def test_book_update():
    client = APIClient()
    author = Author.objects.create(name='Author1')
    genre = Genres.objects.create(name='Fiction')
    book = Book.objects.create(title='OldBook', genre=genre)
    book.authors.add(author)
    url = reverse('book-detail', kwargs={'pk': book.id})

    response = client.put(url, {
        'title': 'NewBook',
        'genre': genre.name,
        'authors': [author.name]
    })

    book.refresh_from_db()
    assert response.status_code == 200
    assert book.title == 'NewBook'
    assert list(book.authors.all()) == [author]


@pytest.mark.django_db
def test_book_delete():
    client = APIClient()
    author = Author.objects.create(name='Author1')
    genre = Genres.objects.create(name='Fiction')
    book = Book.objects.create(title='Book1', genre=genre)
    book.authors.add(author)
    url = reverse('book-detail', kwargs={'pk': book.id})

    response = client.delete(url)
    assert response.status_code == 204
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_genres_creation():
    client = APIClient()
    url = reverse('genres-list')
    response = client.post(url, {'name': 'Mystery'})
    assert response.status_code == 201
    assert Genres.objects.count() == 1
    genre = Genres.objects.first()
    assert genre.name == 'Mystery'


@pytest.mark.django_db
def test_genres_list():
    client = APIClient()
    genres = ['Sci-Fi', 'Mystery', 'Romance']
    [Genres.objects.create(name=genre) for genre in genres]

    url = reverse('genres-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()

    assert len(data['results']) == 3


@pytest.mark.django_db
def test_genres_update():
    client = APIClient()
    genre = Genres.objects.create(name='Mystery')
    url = reverse('genres-detail', kwargs={'pk': genre.id})
    response = client.put(url, {'name': 'Thriller'})

    genre.refresh_from_db()
    assert response.status_code == 200
    assert genre.name == 'Thriller'


@pytest.mark.django_db
def test_genres_delete():
    client = APIClient()
    genre = Genres.objects.create(name='Science Fiction')
    url = reverse('genres-detail', kwargs={'pk': genre.id})

    response = client.delete(url)
    assert response.status_code == 204
    assert Genres.objects.count() == 0
