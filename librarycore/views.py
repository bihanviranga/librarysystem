from django.shortcuts import render
from . import models

def index(request):
    return render(request, "librarycore/index.html", context={"currentNav": "index"})

def books(request):
    books = models.Book.objects.all()
    return render(request, "librarycore/books.html", context={"currentNav": "books", "books":books})

