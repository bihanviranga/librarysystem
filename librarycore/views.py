from django.shortcuts import render
from . import models

def index(request):
    return render(request, "librarycore/index.html")

def books(request):
    books = models.Book.objects.all()
    return render(request, "librarycore/books.html", context={"books":books})

