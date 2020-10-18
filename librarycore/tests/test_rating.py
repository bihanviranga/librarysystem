from django.test import tag
from django.test.utils import setup_test_environment
from django.shortcuts import reverse
from .libraryTestCase import LibraryTestCase
from .helpers import *

@tag('rating', 'rating-crud')
class RatingViewCrudTest(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_createRatingPostRequest(self):
        self.loggedIn = self.createUserAndLogin(1)
        book = getBooks(1)
        url = reverse('rating-create', args=[book.id])
        postDict = {'rating': 10, 'comment': 'sampleComment'}
        response = self.client.post(url, postDict)

        ratingsFromDb = models.BookRating.objects.filter(book=book)

        self.assertTrue(self.loggedIn)
        self.assertEqual(ratingsFromDb.count(), 1)
        self.assertEqual(ratingsFromDb[0].ratings, postDict['rating'])
        self.assertEqual(ratingsFromDb[0].comment, postDict['comment'])

    def test_updateRatingPostRequest(self):
        self.fail()

    def test_deleteRatingPostRequest(self):
        self.fail()

    def test_adminCanDeleteOtherUserRatings(self):
        self.fail()

    def test_userCannotDeleteOtherUserRatings(self):
        self.fail()

    def test_bookDetailPageShowsRatings(self):
        self.fail()

