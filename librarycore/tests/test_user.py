from django.test import tag
from django.test.utils import setup_test_environment
from django.urls import reverse
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('user')
class UserTests(LibraryTestCase):
    def test_cannotAccessUsersPageAsNormalUser(self):
        self.loggedIn = self.createUserAndLogin(1)

        usersUrl = reverse('users')
        usersResponse = self.client.get(usersUrl)

        self.assertTrue(self.loggedIn)
        self.assertEqual(usersResponse.status_code, 403)

    def test_cannotAccessUsersPageWithoutLogin(self):
        loginUrl = reverse('login')
        usersUrl = reverse('users')
        response = self.client.get(usersUrl)

        self.assertFalse(self.loggedIn)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'{loginUrl}?next={usersUrl}')

    def test_canAccessUsersPageAsAdmin(self):
        self.loggedIn = self.createUserAndLogin(1, True)

        url = reverse('users')
        response = self.client.get(url)

        self.assertTrue(self.loggedIn)
        self.assertEqual(response.status_code, 200)

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
        borrowingUser = getUsers(1)
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
        borrowingUser = getUsers(1)
        instance.borrowedBy = borrowingUser
        instance.save()

        self.loggedIn = self.createUserAndLogin(2, True)

        url = reverse('profile', args=[borrowingUser.username])
        response = self.client.get(url)

        userBorrowedBooks = models.BookInstance.objects.filter(borrowedBy__username=borrowingUser.username)

        self.assertTrue(self.loggedIn)
        self.assertEqual(list(userBorrowedBooks), list(response.context['borrowedBooks']))

