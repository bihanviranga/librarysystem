from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .mixins import UserIsAdminMixin

# Utility function
# Currently there's only 1 of these.
# If the num of utility functions grows, will move them
# into a seperate file.
def isUserAdmin(user):
    return user.groups.filter(name='library_admins').exists()

def index(request):
    context={'currentNav': 'index'}

    context['bookCount'] = models.Book.objects.count()
    context['instanceCount'] = models.BookInstance.objects.count()
    context['authorCount'] = models.Author.objects.count()
    context['userCount'] = User.objects.count()
    context['availableCount'] = models.BookInstance.objects.filter(borrowedBy=None).count()
    context['loanCount'] = context['instanceCount'] - context['availableCount']

    if isUserAdmin(request.user):
        context['isAdmin'] = True
    return render(request, "librarycore/index.html", context=context)

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

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True
        return context

class BookUpdate(UserIsAdminMixin, UpdateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = '__all__'

class BooksCreate(UserIsAdminMixin, View):
    def post(self, request):
        bookName = request.POST['bookName']
        bookAuthor = request.POST['bookAuthor']
        try:
            authorInstance = models.Author.objects.get(authorName=bookAuthor)
        except models.Author.DoesNotExist:
            # display author does not exist msg
            # ask the user if they want to create author
            # if yes, redirect to create author page,
            # else, redirect back to books page.
            print("Author does not exist")
            return redirect('books')
        bookInstance = models.Book.objects.create(bookName=bookName, bookAuthor=authorInstance)
        return redirect('books')

class BookInstanceCreate(UserIsAdminMixin, View):
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

        bookInstance = self.get_object()
        if bookInstance.borrowedBy:
            context['isBorrowed'] = True
            if bookInstance.borrowedBy.username == self.request.user.username:
                context['borrowedBySelf'] = True

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True
            if bookInstance.borrowedBy:
                context['borrowedBy'] = bookInstance.borrowedBy.username

        return context

class BookInstanceDelete(UserIsAdminMixin, DeleteView):
    model = models.BookInstance
    context_object_name = "bookInstance"
    success_url = reverse_lazy('books')

class BookInstanceUpdate(UserIsAdminMixin, View):
    def post(self, request, pk):
        instanceSerialNum = request.POST['instanceSerialNum']
        instanceType = request.POST['instanceType']
        instance = models.BookInstance.objects.get(pk=instanceSerialNum)
        instance.instanceType = instanceType
        instance.save()
        return redirect('instance-detail', instanceSerialNum)

class UserSignup(View):
    def get(self, request, **kwargs):
        return render(request,"registration/signup.html")

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/signup.html', {'signup_error':'Username exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'registration/signup.html', {'signup_error':'Email exists'})
        else:
            user = User.objects.create_user(username, email, password)
            # redirect to login with a msg
            return redirect('login')

class UserDetail(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        context = {'profile':user}

        if isUserAdmin(request.user) or request.user.username==user.username:
            borrowedBooks = models.BookInstance.objects.filter(borrowedBy__username=user.username)
            context['borrowedBooks'] = borrowedBooks

        return render(request, "user/profile.html", context)

class UserList(UserIsAdminMixin, ListView):
    model = User
    template_name = 'user/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentNav'] = 'users'
        return context

class BookInstanceBorrow(UserIsAdminMixin, View):
    def post(self, request):
        username = request.POST['borrowingUser']
        user = User.objects.get(username=username)
        bookInstance = models.BookInstance.objects.get(instanceSerialNum=request.POST['bookInstanceId'])
        if not bookInstance.borrowedBy:
            bookInstance.borrowedBy = user
            bookInstance.save()
        return redirect('instance-detail', request.POST['bookInstanceId'])

class BookInstanceReturn(UserIsAdminMixin, View):
    def post(self, request):
        bookInstance = models.BookInstance.objects.get(instanceSerialNum=request.POST['bookInstanceId'])
        bookInstance.borrowedBy = None
        bookInstance.save()
        return redirect('instance-detail', request.POST['bookInstanceId'])

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

