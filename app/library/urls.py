from django.urls import path
from . import views

urlpatterns = [
    path('api/authors/', views.AuthorList.as_view(), name='author-list'),
    path('api/authors/<uuid:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('api/books/', views.BookList.as_view(), name='book-list'),
    path('api/books/<uuid:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('api/genres/', views.GenreList.as_view(), name='genres-list'),
    path('api/genres/<uuid:pk>/', views.GenreDetail.as_view(), name='genres-detail')
]
