from django.shortcuts import render, redirect
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
        return redirect('books')

class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('books')

class BookDetail(DetailView):
    model = models.Book

    # pass book instances as well by overriding this method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        bookInstances = models.BookInstance.objects.filter(instanceBook=book)
        context['instances'] = bookInstances
        bookInstanceTypes = models.BookInstance.INSTANCE_TYPE_CHOICES
        context['instanceTypes'] = bookInstanceTypes
        return context

class BookUpdate(UpdateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = ['bookName', 'bookAuthor']

class BooksCreate(CreateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = '__all__'

class BookInstanceCreate(View):
    def post(self, request):
        instanceType = request.POST['instanceType']
        bookId = request.POST['bookId']
        book = models.Book.objects.get(pk=bookId)
        models.BookInstance.objects.create(instanceBook=book, instanceType=instanceType)
        return redirect('book-detail', bookId)

class BookInstanceDetail(DetailView):
    model = models.BookInstance
    context_object_name = "bookInstance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookInstanceTypes = models.BookInstance.INSTANCE_TYPE_CHOICES
        context['instanceTypes'] = bookInstanceTypes
        return context

class BookInstanceDelete(DeleteView):
    model = models.BookInstance
    context_object_name = "bookInstance"
    success_url = reverse_lazy('books')

class BookInstanceUpdate(View):
    def post(self, request, pk):
        instanceSerialNum = request.POST['instanceSerialNum']
        instanceType = request.POST['instanceType']
        instance = models.BookInstance.objects.get(pk=instanceSerialNum)
        instance.instanceType = instanceType
        instance.save()
        return redirect('instance-detail', instanceSerialNum)

