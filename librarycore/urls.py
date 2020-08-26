from django.urls import path
import librarycore.views as views

urlpatterns = [
    path('', views.index, name='index'),

    path('books', views.Books.as_view(), name='books'),
    path('books/new', views.BooksCreate.as_view(), name='book-create'),
    path('books/<int:pk>', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),

    path('bookinstances/new', views.BookInstanceCreate.as_view(), name='instance-create'),
    path('bookinstances/<str:pk>', views.BookInstanceDetail.as_view(), name='instance-detail'),
    path('bookinstances/<str:pk>/delete', views.BookInstanceDelete.as_view(), name='instance-delete'),
]
