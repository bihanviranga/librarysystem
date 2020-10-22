from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView
from librarycore.mixins import UserIsAdminMixin
from . import models
from .helpers import *

class Books(View):
    def get(self, request):
        context = {'currentNav': 'books'}

        books = models.Book.objects.all()
        contextBooks = []
        for book in books:
            bookDict = book.__dict__
            bookDict['bookAuthor'] = book.bookAuthor.authorName
            bookDict['count'] = models.BookInstance.objects.filter(instanceBook=book).count()
            bookDict['numAvailable'] = models.BookInstance.objects.filter(instanceBook=book).filter(borrowedBy=None).count()
            bookDict['numBorrowed'] = bookDict['count'] - bookDict['numAvailable']
            contextBooks.append(bookDict)

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True

        context['books'] = contextBooks
        return render(request, "librarycore/books.html", context)

class BookDelete(UserIsAdminMixin, DeleteView):
    model = models.Book
    success_url = reverse_lazy('books')

class BookDetail(DetailView):
    model = models.Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        bookInstances = models.BookInstance.objects.filter(instanceBook=book)
        context['instances'] = bookInstances
        bookInstanceTypes = models.BookInstance.INSTANCE_TYPE_CHOICES
        context['instanceTypes'] = bookInstanceTypes
        bookRatings = models.BookRating.objects.filter(book=book)
        context['bookRatings'] = bookRatings

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True
        return context

class BookUpdate(UserIsAdminMixin, UpdateView):
    def get(self, request, pk):
        book = models.Book.objects.get(pk=pk)
        return render(request, 'librarycore/book_form.html', context={'book':book})

class BookCreate(UserIsAdminMixin, View):
    def get(self, request):
        return render(request, 'librarycore/book_form.html')

class BookCreateAndUpdate(UserIsAdminMixin, View):
    def post(self, request):
        bookName = request.POST['bookName']
        bookAuthor = request.POST['bookAuthor']
        if 'bookDescription' in request.POST:
            bookDescription = request.POST['bookDescription']
        else:
            bookDescription = ""

        try:
            authorInstance = models.Author.objects.get(authorName=bookAuthor)
        except models.Author.DoesNotExist:
            # display author does not exist msg
            # ask the user if they want to create author
            # if yes, redirect to create author page,
            # else, redirect back to books page.
            print("Author does not exist")
            return redirect('books')

        if 'bookId' in request.POST:
            models.Book.objects.filter(pk=request.POST['bookId']).update(
                bookName = bookName,
                bookAuthor = authorInstance,
                bookDescription = bookDescription
            )
            bookId = request.POST['bookId']
        else:
            book = models.Book.objects.create(
                bookName = bookName,
                bookAuthor = authorInstance,
                bookDescription = bookDescription
            )
            bookId = book.id

        return redirect('book-detail', bookId)

