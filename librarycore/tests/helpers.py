import random
from django.contrib.auth.models import User, Group
from librarycore import models

# Helper functions for the tests in librarycore

# TODO: getBooks with author or without author? add parameter.
def getBooks(count):
    """
    Returns given number of Book objects.

    The returned Book objects will have a bookName of testingBook1, testingBook2, and so on.
    An author will be created for each book as testingAuthor1, testingAuthor2, and so on.
    The bookDescription field will be blank.

    Parameters:
        count: the number of Book objects to create.

    Returns:
        If count is 1, returns a single object.
        Otherwise returns an array of Book objects.
    """
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
    """
    Returns given number of BookInstance objects.

    Created BookInstance objects will have a randomly created instanceType.

    Parameters:
        count: the number of BookInstance objects to create.
        book: the Book object that should be used as the instanceBook field.

    Returns:
        If count is 1, returns a single object.
        Otherwise returns an array of BookInstance objects.
    """
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

def getUser(n, admin=False):
    """
    Return a User object.

    When n=1, the created User object will have the following attributes:
        Username: testingUser1
        Password: testingPassword1
        Email: testingUser1@email.com

    Parameters:
        n: The number of User objects to create.
        admin: Whether the User should be added to the library_admins group.

    Returns:
        A single User object.
    """
    user = User.objects.create_user(f'testingUser{n}', f'testingUser{n}@email.com', f'testingPassword{n}')
    if admin:
        group = Group.objects.get_or_create(name='library_admins')[0]
        user.groups.add(group)
    return user

def getAuthors(n):
    """
    Returns a given number of Author objects.

    Each Author object will have a name of testingAuthor1, testingAuthor2, and so on.

    Parameters:
        n: The number of Author objects to create.

    Returns:
        If count is 1, returns a single object.
        Otherwise returns an array of Author objects.
    """
    authors = []
    for i in range(n):
        author = models.Author.objects.create(authorName=f'testingAuthor{i}')
        authors.append(author)
    if n == 1:
        return authors[0]
    else:
        return authors

