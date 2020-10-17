from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView
from librarycore.mixins import UserIsAdminMixin
from . import models
from .helpers import *

class AuthorList(View):
    def get(self, request):
        authors = models.Author.objects.all()
        contextAuthors = []
        for author in authors:
            authorDict = author.__dict__
            authorDict['numBooks'] = models.Book.objects.filter(bookAuthor=author).count()
            contextAuthors.append(authorDict)

        context = {'authors': contextAuthors, 'currentNav': 'authors'}

        if isUserAdmin(request.user):
            context['isAdmin'] = True

        return render(request, 'librarycore/authors.html', context)

class AuthorDetail(DetailView):
    model = models.Author
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authorName = self.get_object().authorName
        context['books'] = models.Book.objects.filter(bookAuthor__authorName=authorName)

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True

        return context

class AuthorCreate(UserIsAdminMixin, View):
    def post(self, request):
        authorName = request.POST['authorName']
        models.Author.objects.create(authorName=authorName)
        return redirect('authors')

class AuthorUpdate(UserIsAdminMixin, UpdateView):
    model = models.Author
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('author-detail', args=[self.get_object().pk])

class AuthorDelete(UserIsAdminMixin, View):
    def get(self, request, pk):
        author = models.Author.objects.get(pk=pk)
        context = {"author": author}

        bookCount = models.Book.objects.filter(bookAuthor=author).count()
        if (bookCount):
            instanceCount = models.BookInstance.objects.filter(instanceBook__bookAuthor=author).count()
            context['hasBooks'] = True
            context['bookCount'] = bookCount
            context['instanceCount'] = instanceCount

        return render(request, 'librarycore/author_confirm_delete.html', context=context)

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        author = models.Author.objects.get(pk=pk).delete()
        return redirect('authors')

