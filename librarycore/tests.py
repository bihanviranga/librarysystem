import random
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse
from django.contrib.auth.models import User, Group
from librarycore import models

# TODO: Test NotFound errors in GET and DELETE and UPDATE

def getBooks(count):
    books = []
    for i in range(count):
        bookName = f'testingBook{i}'
        bookAuthor = f'testingAuthor{i}'
        book = models.Book.objects.create(bookName=bookName, bookAuthor=bookAuthor)
        books.append(book)
    return books

def getBookInstances(count, book):
    bookInstances = []
    for i in range(count):
        instanceBook = book
        instanceType = random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES)[0]
        instance = models.BookInstance.objects.create(instanceBook=instanceBook, instanceType=instanceType)
        bookInstances.append(instance)
    return bookInstances

def getUser(n, admin=False):
    user = User.objects.create_user(f'testingUser{n}', f'testingUser{n}@email.com', f'testingPassword{n}')
    if admin:
        group = Group.objects.get_or_create(name='library_admins')[0]
        user.groups.add(group)
    return user

class GeneralSiteTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_indexHasCurrentNavSet(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.context['currentNav'], 'index')

class BookViewTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_createBookPostRequest(self):
        url = reverse('book-create')
        postDict = {'bookName': 'testingBook', 'bookAuthor':'testingAuthor', 'bookDescription':'testingDescription'}
        response = self.client.post(url, postDict)
        bookFromDb = models.Book.objects.all()[0]
        self.assertEqual(bookFromDb.bookName, postDict['bookName'])
        self.assertEqual(bookFromDb.bookAuthor, postDict['bookAuthor'])

    def test_booksPageHasCurrentNavSet(self):
        url = reverse('books')
        response = self.client.get(url)
        self.assertEqual(response.context['currentNav'], 'books')

    def test_bookDetailPageHasBookInstances(self):
        book1 = getBooks(1)[0]
        instances = getBookInstances(3, book1)
        url = reverse('book-detail', args=[book1.id])
        response = self.client.get(url)
        querysetFromContext = list(response.context['instances'])
        self.assertEqual(querysetFromContext, instances)

    def test_bookDetailPageHasBookInstanceTypes(self):
        book1 = getBooks(1)[0]
        url = reverse('book-detail', args=[book1.id])
        response = self.client.get(url)
        self.assertEqual(response.context['instanceTypes'], models.BookInstance.INSTANCE_TYPE_CHOICES)

class BookInstanceViewTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_createBookInstancePostRequest(self):
        book1 = getBooks(1)[0]
        url = reverse('instance-create')
        postDict = {'instanceType': random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES[0]), 'bookId': str(book1.id)}
        response = self.client.post(url, postDict)
        instanceFromDb = models.BookInstance.objects.all()[0]
        self.assertEqual(instanceFromDb.instanceType, postDict['instanceType'])
        self.assertEqual(instanceFromDb.instanceBook, book1)

    def test_updateBookInstancePostRequest(self):
        book1 = getBooks(1)[0]
        instance1 = getBookInstances(1, book1)[0]
        url = reverse('instance-update', args=[instance1.instanceSerialNum])
        postInstanceType = random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES)[0]
        postDict = {'instanceSerialNum': instance1.instanceSerialNum, 'instanceType': postInstanceType}
        response = self.client.post(url, postDict)
        instanceFromDb = models.BookInstance.objects.get(pk=postDict['instanceSerialNum'])
        self.assertEqual(instanceFromDb.instanceType, postDict['instanceType'])

    def test_bookInstancePageHasInstanceTypes(self):
        book1 = getBooks(1)[0]
        instance = getBookInstances(1, book1)[0]
        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)
        self.assertEqual(response.context['instanceTypes'], models.BookInstance.INSTANCE_TYPE_CHOICES)

class UserTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_accessUsersPageAsNormalUser(self):
        user = getUser(1, False)

        loggedIn = self.client.login(username='testingUser1', password='testingPassword1')

        usersUrl = reverse('users')
        usersResponse = self.client.get(usersUrl)

        self.assertTrue(loggedIn)
        self.assertEqual(usersResponse.status_code, 403)

    def test_accessUsersPageWithoutLogin(self):
        loginUrl = reverse('login')
        usersUrl = reverse('users')
        response = self.client.get(usersUrl)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'{loginUrl}?next={usersUrl}')

    def test_accessUsersPageAsAdmin(self):
        admin = getUser(1, True)

        loggedIn = self.client.login(username='testingUser1', password='testingPassword1')

        usersUrl = reverse('users')
        usersResponse = self.client.get(usersUrl)

        self.assertTrue(loggedIn)
        self.assertEqual(usersResponse.status_code, 200)

