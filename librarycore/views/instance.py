from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView, DeleteView
from librarycore.mixins import UserIsAdminMixin
from . import models
from .helpers import *

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

