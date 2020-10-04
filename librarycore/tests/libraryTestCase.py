from django.test import TestCase
from .helpers import *

class LibraryTestCase(TestCase):
    loggedIn = False
    user = None

    def createUserAndLogin(self, n, admin=False):
        user = getUsers(n, admin)
        self.user = user
        loggedIn = self.client.login(username=f'testingUser{n}', password=f'testingPassword{n}')
        return loggedIn

    def tearDown(self):
        if self.loggedIn:
            self.client.logout()
            self.loggedIn = False

