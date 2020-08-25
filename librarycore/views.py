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

