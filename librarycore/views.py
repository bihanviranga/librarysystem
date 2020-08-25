from django.shortcuts import render
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from . import models

def index(request):
    return render(request, "librarycore/index.html", context={"currentNav": "index"})

class Books(View):
    def get(self, request):
        books = models.Book.objects.all()
        return render(request, "librarycore/books.html", context={"currentNav": "books", "books":books})

    def post(self, request):
        bookName = request.POST['bookName']
        authorName = request.POST['authorName']
        models.Book.objects.create(bookName=bookName, bookAuthor=authorName)
        books = models.Book.objects.all()
        return render(request, "librarycore/books.html", context={"currentNav": "books", "books":books})

class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('books')

class BookDetail(DetailView):
    model = models.Book

class BookUpdate(UpdateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = ['bookName', 'bookAuthor']

class BooksCreate(CreateView):
    model = models.Book
    fields = '__all__'
