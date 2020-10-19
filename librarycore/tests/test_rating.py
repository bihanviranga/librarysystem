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
        self.loggedIn = self.createUserAndLogin(1)
        book = getBooks(1)
        rating = models.BookRating.objects.create(
            user=self.user,
            book=book,
            comment="testingComment",
            ratings=1
        )

        url = reverse('rating-update', args=[rating.id])
        postDict = {'comment': 'updatedComment', 'rating': 10}
        response = self.client.post(url, postDict)

        rating = models.BookRating.objects.get(pk=rating.id)

        self.assertTrue(self.loggedIn)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.book, book)
        self.assertEqual(rating.comment, postDict['comment'])
        self.assertEqual(rating.ratings, postDict['rating'])


    def test_deleteRatingPostRequest(self):
        self.fail()

    def test_adminCanDeleteOtherUserRatings(self):
        self.fail()

    def test_userCannotDeleteOtherUserRatings(self):
        self.fail()

    def test_bookDetailPageShowsRatings(self):
        book = getBooks(1)
        user = getUsers(1)
        r1 = models.BookRating.objects.create(book=book, user=user, ratings=1, comment="testingComment1")
        r2 = models.BookRating.objects.create(book=book, user=user, ratings=2, comment="testingComment2")
        r3 = models.BookRating.objects.create(book=book, user=user, ratings=3, comment="testingComment3")

        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)

        self.assertEqual(list(response.context['bookRatings']), [r1, r2, r3])

