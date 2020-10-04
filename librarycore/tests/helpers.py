import random
from django.contrib.auth.models import User, Group
from librarycore import models

# Helper functions for the tests in librarycore

# TODO: getBooks with author or without author? add parameter.
def getBooks(count):
    books = []
    for i in range(count):
        bookName = f'testingBook{i}'
        bookAuthor =  models.Author.objects.create(authorName=f'testingAuthor{i}')
        book = models.Book.objects.create(bookName=bookName, bookAuthor=bookAuthor)
        books.append(book)
    if count == 1:
        return books[0]
    else:
        return books

def getBookInstances(count, book):
    bookInstances = []
    for i in range(count):
        instanceBook = book
        instanceType = random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES)[0]
        instance = models.BookInstance.objects.create(instanceBook=instanceBook, instanceType=instanceType)
        bookInstances.append(instance)
    if count == 1:
        return bookInstances[0]
    else:
        return bookInstances

def getUsers(n, admin=False):
    user = User.objects.create_user(f'testingUser{n}', f'testingUser{n}@email.com', f'testingPassword{n}')
    if admin:
        group = Group.objects.get_or_create(name='library_admins')[0]
        user.groups.add(group)
    return user

def getAuthors(n):
    authors = []
    for i in range(n):
        author = models.Author.objects.create(authorName=f'testingAuthor{i}')
        authors.append(author)
    if n == 1:
        return authors[0]
    else:
        return authors

