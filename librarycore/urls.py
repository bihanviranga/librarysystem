from django.urls import path
import librarycore.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.Books.as_view(), name='books'),
    path('books/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>', views.BookDetail.as_view(), name='book-detail'),
]
