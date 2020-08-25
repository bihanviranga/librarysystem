from django.urls import path
import librarycore.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.Books.as_view(), name='books'),
]
