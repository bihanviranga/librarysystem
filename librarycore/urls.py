from django.urls import path
import librarycore.views as views

urlpatterns = [
    path('', views.index),
    path('books', views.books, name='books'),
]
