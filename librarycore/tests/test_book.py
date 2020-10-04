from django.test import tag
from django.test.utils import setup_test_environment
from django.urls import reverse
from librarycore import models
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('book')
class BookViewTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_createBookPostRequestAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        author = models.Author.objects.create(authorName='testingAuthor')

        url = reverse('book-create')
        postDict = {'bookName': 'testingBook', 'bookAuthor':'testingAuthor', 'bookDescription':'testingDescription'}
        response = self.client.post(url, postDict)
        bookFromDb = models.Book.objects.all()[0]

        self.assertTrue(self.loggedIn)
        self.assertEqual(bookFromDb.bookName, postDict['bookName'])
        self.assertEqual(bookFromDb.bookAuthor.authorName, postDict['bookAuthor'])

    def test_createBookPostRequestAsUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        author = models.Author.objects.create(authorName='testingAuthor')

        url = reverse('book-create')
        postDict = {'bookName':'testingBook', 'bookAuthor':'testingAuthor', 'bookDescription':'testingDescription'}
        response = self.client.post(url, postDict)
        booksInDb = models.Book.objects.all().count()

        self.assertTrue(self.loggedIn)
        self.assertEqual(booksInDb, 0)

    def test_createBookPostRequestWithoutLogin(self):
        author = models.Author.objects.create(authorName='testingAuthor')

        url = reverse('book-create')
        postDict = {'bookName':'testingBook', 'bookAuthor':'testingAuthor', 'bookDescription':'testingDescription'}
        response = self.client.post(url, postDict)
        booksInDb = models.Book.objects.all().count()

        self.assertFalse(self.loggedIn)
        self.assertEqual(booksInDb, 0)

    def test_booksPageHasCurrentNavSet(self):
        url = reverse('books')
        response = self.client.get(url)

        self.assertEqual(response.context['currentNav'], 'books')

    def test_bookDetailPageHasBookInstances(self):
        book1 = getBooks(1)
        instances = getBookInstances(3, book1)

        url = reverse('book-detail', args=[book1.id])
        response = self.client.get(url)
        querysetFromContext = list(response.context['instances'])

        self.assertEqual(querysetFromContext, instances)

    def test_bookDetailPageHasBookInstanceTypes(self):
        book1 = getBooks(1)
        url = reverse('book-detail', args=[book1.id])
        response = self.client.get(url)

        self.assertEqual(response.context['instanceTypes'], models.BookInstance.INSTANCE_TYPE_CHOICES)

    def test_booksPageShowsBooksCounts(self):
        book = getBooks(1)
        instances = getBookInstances(5, book)
        user = getUsers(1)
        instances[0].borrowedBy = user
        instances[0].save()
        instances[1].borrowedBy = user
        instances[1].save()

        url = reverse('books')
        response = self.client.get(url)
        bookFromResponse = response.context['books'][0]

        self.assertEqual(bookFromResponse['count'], 5)
        self.assertEqual(bookFromResponse['numAvailable'], 3)
        self.assertEqual(bookFromResponse['numBorrowed'], 2)

    def test_booksPageShowsBookInformation(self):
        books = getBooks(2)
        url = reverse('books')
        response = self.client.get(url)

        self.assertContains(response, books[0].bookName)
        self.assertContains(response, books[0].bookAuthor.authorName)
        self.assertContains(response, books[1].bookName)
        self.assertContains(response, books[1].bookAuthor.authorName)

    def test_bookDetailsPageShowsBookInformation(self):
        book = getBooks(1)
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)

        self.assertContains(response, book.bookName)
        self.assertContains(response, book.bookAuthor.authorName)

