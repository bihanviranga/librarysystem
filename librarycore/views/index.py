from django.contrib.auth.models import User
from django.shortcuts import render
from librarycore import models
from .helpers import *

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

