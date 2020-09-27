import random
from django.test import TestCase, tag
from django.test.utils import setup_test_environment
from django.urls import reverse
from django.contrib.auth.models import User, Group
from librarycore import models

# TODO: Test NotFound errors in GET and DELETE and UPDATE

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

def getUser(n, admin=False):
    user = User.objects.create_user(f'testingUser{n}', f'testingUser{n}@email.com', f'testingPassword{n}')
    if admin:
        group = Group.objects.get_or_create(name='library_admins')[0]
        user.groups.add(group)
    return user

def getAuthor(n):
    authors = []
    for i in range(n):
        author = models.Author.objects.create(authorName=f'testingAuthor{i}')
        authors.append(author)
    if n == 1:
        return authors[0]
    else:
        return authors

class LibraryTestCase(TestCase):
    loggedIn = False
    user = None

    def createUserAndLogin(self, n, admin=False):
        user = getUser(n, admin)
        self.user = user
        loggedIn = self.client.login(username=f'testingUser{n}', password=f'testingPassword{n}')
        return loggedIn

    def tearDown(self):
        if self.loggedIn:
            self.client.logout()
            self.loggedIn = False

@tag('general')
class GeneralSiteTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_indexHasCurrentNavSet(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.context['currentNav'], 'index')

@tag('book')
class BookViewTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_createBookPostRequest(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        author = models.Author.objects.create(authorName='testingAuthor')

        url = reverse('book-create')
        postDict = {'bookName': 'testingBook', 'bookAuthor':'testingAuthor', 'bookDescription':'testingDescription'}
        response = self.client.post(url, postDict)
        bookFromDb = models.Book.objects.all()[0]

        self.assertTrue(self.loggedIn)
        self.assertEqual(bookFromDb.bookName, postDict['bookName'])
        self.assertEqual(bookFromDb.bookAuthor.authorName, postDict['bookAuthor'])

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
        user = getUser(1)
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

@tag('book-instance')
class BookInstanceViewTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_createBookInstancePostRequest(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        book1 = getBooks(1)
        url = reverse('instance-create')
        postDict = {'instanceType': random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES[0]), 'bookId': str(book1.id)}
        response = self.client.post(url, postDict)
        instanceFromDb = models.BookInstance.objects.all()[0]

        self.assertTrue(self.loggedIn)
        self.assertEqual(instanceFromDb.instanceType, postDict['instanceType'])
        self.assertEqual(instanceFromDb.instanceBook, book1)

    def test_updateBookInstancePostRequest(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        book1 = getBooks(1)
        instance1 = getBookInstances(1, book1)
        url = reverse('instance-update', args=[instance1.instanceSerialNum])
        postInstanceType = random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES)[0]
        postDict = {'instanceSerialNum': instance1.instanceSerialNum, 'instanceType': postInstanceType}
        response = self.client.post(url, postDict)
        instanceFromDb = models.BookInstance.objects.get(pk=postDict['instanceSerialNum'])

        self.assertTrue(self.loggedIn)
        self.assertEqual(instanceFromDb.instanceType, postDict['instanceType'])

    def test_bookInstancePageHasInstanceTypes(self):
        book1 = getBooks(1)
        instance = getBookInstances(1, book1)
        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)
        self.assertEqual(response.context['instanceTypes'], models.BookInstance.INSTANCE_TYPE_CHOICES)

    def test_adminCanMarkInstancesAsBorrowed(self):
        self.loggedIn = self.createUserAndLogin(1, True)
        borrowingUser = getUser(2)
        book = getBooks(1)
        instance = getBookInstances(1, book)

        url = reverse('instance-borrow')
        postDict = {'bookInstanceId': instance.instanceSerialNum, 'borrowingUser': borrowingUser}
        response = self.client.post(url, postDict)

        # 'refresh' the instance obj
        instance = models.BookInstance.objects.get(pk=instance.instanceSerialNum)

        self.assertTrue(self.loggedIn)
        self.assertEqual(instance.borrowedBy.username, borrowingUser.username)

    def test_adminCannotBorrowAlreadyBorrowedBookInstances(self):
        borrowingUser = getUser(1)
        borrowingUser2 = getUser(2)
        book = getBooks(1)
        instance = getBookInstances(1, book)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(3, True)
        url = reverse('instance-borrow')
        postDict = {'bookInstanceId': instance.instanceSerialNum, 'borrowingUser': borrowingUser2}
        response = self.client.post(url, postDict)

        instance = models.BookInstance.objects.get(pk=instance.instanceSerialNum)

        self.assertTrue(self.loggedIn)
        self.assertEqual(instance.borrowedBy.username, borrowingUser.username)

    def test_adminCanMarkBookInstancesAsReturned(self):
        self.loggedIn = self.createUserAndLogin(1, True)
        user = getUser(2)
        book = getBooks(1)
        instance = getBookInstances(1, book)
        instance.borrowedBy = user
        instance.save()

        url = reverse('instance-return')
        postDict = {'bookInstanceId': instance.instanceSerialNum}
        response = self.client.post(url, postDict)

        instance = models.BookInstance.objects.get(pk=instance.instanceSerialNum)

        self.assertTrue(self.loggedIn)
        self.assertIsNone(instance.borrowedBy)

    def test_cannotBorrowBookInstancesWithoutLogin(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)

        url = reverse('instance-borrow')
        postDict = {'bookInstanceId':instance.instanceSerialNum}
        response = self.client.post(url, postDict)

        instance = models.BookInstance.objects.get(pk=instance.instanceSerialNum)

        self.assertFalse(self.loggedIn)
        self.assertIsNone(instance.borrowedBy)

    def test_userCanSeeWhetherInstanceIsBorrowed(self):
        book = getBooks(1)
        instance1, instance2 = getBookInstances(2, book)
        borrowingUser = getUser(1)
        instance1.borrowedBy = borrowingUser
        instance1.save()

        self.loggedIn = self.createUserAndLogin(2, True)

        url1 = reverse('instance-detail', args=[instance1.instanceSerialNum])
        response1 = self.client.get(url1)

        url2 = reverse('instance-detail', args=[instance2.instanceSerialNum])
        response2 = self.client.get(url2)

        self.assertTrue(self.loggedIn)
        self.assertIn('isBorrowed', response1.context.keys())
        self.assertNotIn('isBorrowed', response2.context.keys())

    def test_adminCanSeeWhoBorrowedInstance(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        borrowingUser = getUser(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2, True)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertEquals(response.context['borrowedBy'], borrowingUser.username)

    def test_normalUsersCannotSeeWhoBorrowedInstance(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        borrowingUser = getUser(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertNotIn('borrowedBy', response.context.keys())

@tag('user')
class UserTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_accessUsersPageAsNormalUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        usersUrl = reverse('users')
        usersResponse = self.client.get(usersUrl)

        self.assertTrue(self.loggedIn)
        self.assertEqual(usersResponse.status_code, 403)

    def test_accessUsersPageWithoutLogin(self):
        loginUrl = reverse('login')
        usersUrl = reverse('users')
        response = self.client.get(usersUrl)
        self.assertFalse(self.loggedIn)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'{loginUrl}?next={usersUrl}')

    def test_accessUsersPageAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        usersUrl = reverse('users')
        usersResponse = self.client.get(usersUrl)

        self.assertTrue(self.loggedIn)
        self.assertEqual(usersResponse.status_code, 200)

    def test_userCanSeeOwnBorrowedBooks(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        self.loggedIn = self.createUserAndLogin(1)
        instance.borrowedBy = self.user
        instance.save()

        url = reverse('profile', args=[self.user.username])
        response = self.client.get(url)

        userBorrowedBooks = models.BookInstance.objects.filter(borrowedBy__username=self.user.username)

        self.assertTrue(self.loggedIn)
        self.assertEqual(list(userBorrowedBooks), list(response.context['borrowedBooks']))

    def test_userCannotSeeOtherUserBorrowedBooks(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        borrowingUser = getUser(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2)

        url = reverse('profile', args=[borrowingUser.username])
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertNotIn('borrowedBooks', response.context.keys())

    def test_adminCanSeeUserBorrowedBooks(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        borrowingUser = getUser(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2, True)

        url = reverse('profile', args=[borrowingUser.username])
        response = self.client.get(url)

        userBorrowedBooks = models.BookInstance.objects.filter(borrowedBy__username=borrowingUser.username)

        self.assertTrue(self.loggedIn)
        self.assertEquals(list(userBorrowedBooks), list(response.context['borrowedBooks']))

@tag('author')
class AuthorViewTests(LibraryTestCase):
    def test_authorListPageHasCurrentNavSet(self):
        url = reverse('authors')
        response = self.client.get(url)

        self.assertEquals(response.context['currentNav'], 'authors')

    def test_authorListPageShowsAuthorsList(self):
        authors = getAuthor(2)
        url = reverse('authors')
        response = self.client.get(url)

        self.assertContains(response, authors[0].authorName)
        self.assertContains(response, authors[1].authorName)

