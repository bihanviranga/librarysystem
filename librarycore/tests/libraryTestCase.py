from django.test import TestCase
from django.test.utils import setup_test_environment
from .helpers import *

class LibraryTestCase(TestCase):
    loggedIn = False
    user = None

    def setup(self):
        setup_test_environment()

    def createUserAndLogin(self, n, admin=False):
        user = getUser(n, admin)
        self.user = user
        loggedIn = self.client.login(username=f'testingUser{n}', password=f'testingPassword{n}')
        return loggedIn

    def tearDown(self):
        if self.loggedIn:
            self.client.logout()
            self.loggedIn = False

