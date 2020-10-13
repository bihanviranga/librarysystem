from django.test import tag, TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse
from .helpers import *

@tag('general')
class GeneralSiteTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_indexHasCurrentNavSet(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.context['currentNav'], 'index')

    def test_dashboardShowsStatus(self):
        books = getBooks(3)
        book1instances = getBookInstances(2, books[0])
        book2instances = getBookInstances(5, books[1])
        newAuthor = getAuthors(1)
        user1 = getUsers(1)
        user2 = getUsers(2)
        book1instances[0].borrowedBy = user1
        book1instances[0].save()
        book2instances[1].borrowedBy = user2
        book2instances[1].save()

        # 3 books
        # 7 instances
        # 4 authors
        # 2 users + 1 default admin user created in the migration
        # 2 on loan
        # 5 available

        url = reverse('index')
        response = self.client.get(url)


        self.assertEqual(response.context['bookCount'], 3)
        self.assertEqual(response.context['instanceCount'], 7)
        self.assertEqual(response.context['authorCount'], 4)
        self.assertEqual(response.context['availableCount'], 5)
        self.assertEqual(response.context['loanCount'], 2)
        self.assertEqual(response.context['userCount'], 3)

