from django.test import tag
from django.urls import reverse
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('author')
class AuthorViewTests(LibraryTestCase):
    def test_authorListPageHasCurrentNavSet(self):
        url = reverse('authors')
        response = self.client.get(url)

        self.assertEqual(response.context['currentNav'], 'authors')

    def test_authorListPageShowsAuthorsList(self):
        authors = getAuthors(2)
        url = reverse('authors')
        response = self.client.get(url)

        self.assertContains(response, authors[0].authorName)
        self.assertContains(response, authors[1].authorName)

    def test_authorDetailsPageShowsAuthorDetails(self):
        author = getAuthors(1)
        url = reverse('author-detail', args=[author.id])
        response = self.client.get(url)

        self.assertEqual(response.context['author'], author)

    def test_authorDetailsPageShowsAuthorBooks(self):
        books = getBooks(2)
        author = getAuthors(1)
        books[0].bookAuthor = books[1].bookAuthor = author
        books[0].save()
        books[1].save()

        url = reverse('author-detail', args=[author.id])
        response = self.client.get(url)

        self.assertEqual(list(response.context['books']), list(books))

    def test_createAuthorPostRequestAsUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        authors = getAuthors(2)
        url = reverse('author-create')
        postDict = {'authorName': 'fakeAuthorName'}
        response = self.client.post(url, postDict)

        authorsFromDb = models.Author.objects.filter(authorName='fakeAuthorName')

        self.assertTrue(self.loggedIn)
        self.assertEqual(authorsFromDb.count(), 0)

    def test_createAuthorPostRequestAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        authors = getAuthors(2)
        url = reverse('author-create')
        postDict = {'authorName': 'fakeAuthorName'}
        response = self.client.post(url, postDict)

        authorsFromDb = models.Author.objects.filter(authorName='fakeAuthorName')

        self.assertTrue(self.loggedIn)
        self.assertEqual(authorsFromDb.count(), 1)

    def test_createAuthorPostRequestWithoutLogin(self):
        authors = getAuthors(2)
        url = reverse('author-create')
        postDict = {'authorName': 'fakeAuthorName'}
        response = self.client.post(url, postDict)

        authorsFromDb = models.Author.objects.filter(authorName='fakeAuthorName')

        self.assertFalse(self.loggedIn)
        self.assertEqual(authorsFromDb.count(), 0)

