from django.test import tag
from django.test.utils import setup_test_environment
from django.urls import reverse
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('book-instance', 'book-instance-crud')
class BookInstanceViewCrudTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_viewBookInstanceDetails(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertEqual(response.context['bookInstance'], instance)

    def test_createBookInstancePostRequestAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        book1 = getBooks(1)
        url = reverse('instance-create')
        postDict = {'instanceType': random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES[0]), 'bookId': str(book1.id)}
        response = self.client.post(url, postDict)
        instanceFromDb = models.BookInstance.objects.all()[0]

        self.assertTrue(self.loggedIn)
        self.assertEqual(instanceFromDb.instanceType, postDict['instanceType'])
        self.assertEqual(instanceFromDb.instanceBook, book1)

    def test_createBookInstancePostRequestAsUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        book1 = getBooks(1)
        url = reverse('instance-create')
        postDict = {'instanceType': random.choice(models.BookInstance.INSTANCE_TYPE_CHOICES[0]), 'bookId': str(book1.id)}
        response = self.client.post(url, postDict)
        instancesFromDb = models.BookInstance.objects.all().count()

        self.assertTrue(self.loggedIn)
        self.assertEqual(instancesFromDb, 0)

    def test_updateBookInstancePostRequestAsAdmin(self):
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

    def test_updateBookInstancePostRequestAsUser(self):
        self.fail()

    def test_deleteBookInstancePostRequestAsAdmin(self):
        self.fail()

    def test_deleteBookInstancePostRequestAsUser(self):
        self.fail()

@tag('book-instance')
class BookInstanceViewTests(LibraryTestCase):
    def setup(self):
        setup_test_environment()


    def test_bookInstancePageHasInstanceTypes(self):
        book1 = getBooks(1)
        instance = getBookInstances(1, book1)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertEqual(response.context['instanceTypes'], models.BookInstance.INSTANCE_TYPE_CHOICES)

    # TODO: control tests
    def test_adminCanMarkInstancesAsBorrowed(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        borrowingUser = getUsers(2)
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
        borrowingUser = getUsers(1)
        borrowingUser2 = getUsers(2)
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
        user = getUsers(2)
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
        borrowingUser = getUsers(1)
        instance1.borrowedBy = borrowingUser
        instance1.save()

        self.loggedIn = self.createUserAndLogin(2)

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
        borrowingUser = getUsers(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2, True)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertTrue(response.context['isAdmin'])
        self.assertEquals(response.context['borrowedBy'], borrowingUser.username)

    def test_normalUsersCannotSeeWhoBorrowedInstance(self):
        book = getBooks(1)
        instance = getBookInstances(1, book)
        borrowingUser = getUsers(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2)

        url = reverse('instance-detail', args=[instance.instanceSerialNum])
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertNotIn('borrowedBy', response.context.keys())

