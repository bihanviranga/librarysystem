from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView, ListView
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
    return render(request, "librarycore/index.html", context={"currentNav": "index"})

class Books(ListView):
    model = models.Book
    template_name = "librarycore/books.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentNav'] = 'books'

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True
        return context

class BookDelete(UserIsAdminMixin, DeleteView):
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

        if isUserAdmin(self.request.user):
            context['isAdmin'] = True
        return context

class BookUpdate(UserIsAdminMixin, UpdateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = '__all__'

class BooksCreate(UserIsAdminMixin, CreateView):
    model = models.Book
    success_url = reverse_lazy('books')
    fields = '__all__'

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
        return render(request, "user/profile.html", {'profile':user})

class UserList(UserIsAdminMixin, ListView):
    model = User
    template_name = 'user/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentNav'] = 'users'
        return context

class BookInstanceBorrow(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        bookInstance = models.BookInstance.objects.get(instanceSerialNum=request.POST['bookInstanceId'])
        if not bookInstance.borrowedBy:
            bookInstance.borrowedBy = user
            bookInstance.save()
        return redirect('instance-detail', request.POST['bookInstanceId'])

class BookInstanceReturn(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        bookInstance = models.BookInstance.objects.get(instanceSerialNum=request.POST['bookInstanceId'])
        if bookInstance.borrowedBy == user:
            bookInstance.borrowedBy = None
            bookInstance.save()
        return redirect('instance-detail', request.POST['bookInstanceId'])

