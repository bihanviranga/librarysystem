from django.shortcuts import render
from django.views import View
from . import models

def index(request):
    return render(request, "librarycore/index.html", context={"currentNav": "index"})

# def books(request):
    # books = models.Book.objects.all()
    # return render(request, "librarycore/books.html", context={"currentNav": "books", "books":books})

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
