from django.test import tag
from django.test.utils import setup_test_environment
from django.urls import reverse
from librarycore import models
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('book', 'book-crud')
class BookViewCrudTest(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_bookDetailsPageShowsBookInformation(self):
        book = getBooks(1)
        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)

        self.assertContains(response, book.bookName)
        self.assertContains(response, book.bookAuthor.authorName)

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

    def test_updateBookPostRequestAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        book1 = getBooks(1)
        author2 = models.Author.objects.create(authorName="updatedAuthor")

        url = reverse('book-update', args=[book1.id])
        postDict = {"id":book1.id, "bookName":"updatedBookName", "bookDescription":"updatedBookDescription", "bookAuthor":author2.id}
        response = self.client.post(url, postDict)

        book1 = models.Book.objects.get(pk=book1.id)

        self.assertEqual(book1.bookName, postDict['bookName'])
        self.assertEqual(book1.bookDescription, postDict['bookDescription'])
        self.assertEqual(book1.bookAuthor.authorName, author2.authorName)

    def test_updateBookPostRequestAsUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        book1 = getBooks(1)
        origBookName = book1.bookName
        origBookDescription = book1.bookDescription
        origBookAuthorName = book1.bookAuthor.authorName
        author2 = models.Author.objects.create(authorName="updatedAuthor")

        url = reverse('book-update', args=[book1.id])
        postDict = {"id": book1.id, "bookName":"updatedBookName", "bookDescription":"updatedBookDescription", "bookAuthor":author2.id}
        response = self.client.post(url, postDict)

        book1 = models.Book.objects.get(pk=book1.id)

        self.assertEqual(book1.bookName, origBookName)
        self.assertEqual(book1.bookDescription, origBookDescription)
        self.assertEqual(book1.bookAuthor.authorName, origBookAuthorName)

    def test_updateBookPostRequestWithoutLogin(self):
        book1 = getBooks(1)
        origBookName = book1.bookName
        origBookDescription = book1.bookDescription
        origBookAuthorName = book1.bookAuthor.authorName
        author2 = models.Author.objects.create(authorName="updatedAuthor")

        url = reverse('book-update', args=[book1.id])
        postDict = {"id": book1.id, "bookName":"updatedBookName", "bookDescription":"updatedBookDescription", "bookAuthor":author2.id}
        response = self.client.post(url, postDict)

        book1 = models.Book.objects.get(pk=book1.id)

        self.assertEqual(book1.bookName, origBookName)
        self.assertEqual(book1.bookDescription, origBookDescription)
        self.assertEqual(book1.bookAuthor.authorName, origBookAuthorName)

    def test_deleteBookPostRequestAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        books = getBooks(3)

        url = reverse('book-delete', args=[books[0].id])
        response = self.client.post(url)

        booksFromDb = models.Book.objects.all()

        self.assertNotIn(books[0], booksFromDb)
        self.assertEqual(booksFromDb.count(), 2)

    def test_deleteBookPostRequestAsUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        books = getBooks(3)

        url = reverse('book-delete', args=[books[0].id])
        response = self.client.post(url)

        booksFromDb = models.Book.objects.all()

        self.assertIn(books[0], booksFromDb)
        self.assertEqual(booksFromDb.count(), 3)

    def test_deleteBookPostRequestWithoutLogin(self):
        books = getBooks(3)

        url = reverse('book-delete', args=[books[0].id])
        response = self.client.post(url)

        booksFromDb = models.Book.objects.all()

        self.assertIn(books[0], booksFromDb)
        self.assertEqual(booksFromDb.count(), 3)

@tag('book')
class BookViewTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

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


