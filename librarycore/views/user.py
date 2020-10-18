from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from librarycore.mixins import UserIsAdminMixin
from . import models
from .helpers import *

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

