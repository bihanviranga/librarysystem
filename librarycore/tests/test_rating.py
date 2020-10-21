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
        postDict = {'score': 10, 'comment': 'sampleComment'}
        response = self.client.post(url, postDict)

        ratingsFromDb = models.BookRating.objects.filter(book=book)

        self.assertTrue(self.loggedIn)
        self.assertEqual(ratingsFromDb.count(), 1)
        self.assertEqual(ratingsFromDb[0].score, postDict['score'])
        self.assertEqual(ratingsFromDb[0].comment, postDict['comment'])

    def test_updateRatingPostRequest(self):
        self.loggedIn = self.createUserAndLogin(1)
        book = getBooks(1)
        rating = models.BookRating.objects.create(
            user=self.user,
            book=book,
            comment="testingComment",
            score=1
        )

        url = reverse('rating-update', args=[rating.id])
        postDict = {'comment': 'updatedComment', 'score': 10}
        response = self.client.post(url, postDict)

        rating = models.BookRating.objects.get(pk=rating.id)

        self.assertTrue(self.loggedIn)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.book, book)
        self.assertEqual(rating.comment, postDict['comment'])
        self.assertEqual(rating.score, postDict['score'])

    def test_canUpdateOnlyOwnRatings(self):
        user = getUsers(2)
        book = getBooks(1)
        rating = models.BookRating.objects.create(book=book, user=user, score=1, comment="originalComment1")

        url = reverse('rating-update', args=[rating.id])

        self.loggedIn = self.createUserAndLogin(1)
        postDictUser = {'comment': 'userComment', 'score': 2}
        responseUser = self.client.post(url, postDictUser)
        self.client.logout()

        self.loggedIn = self.createUserAndLogin(3, True)
        postDictAdmin = {'comment': 'adminComment', 'score': 3}
        responseAdmin = self.client.post(url, postDictAdmin)
        self.client.logout()

        rating = models.BookRating.objects.get(pk=rating.id)

        self.assertEqual(rating.comment, 'originalComment1')
        self.assertEqual(rating.score, 1)

    def test_userCanDeleteOwnRatingPostRequest(self):
        self.loggedIn = self.createUserAndLogin(1)
        book = getBooks(1)
        rating = models.BookRating.objects.create(book=book, user=self.user, score=1, comment="testingComment1")

        url = reverse('rating-delete', args=[rating.id])
        response = self.client.get(url)

        ratings = models.BookRating.objects.filter(book=book)

        self.assertTrue(self.loggedIn)
        self.assertEqual(ratings.count(), 0)
        self.assertNotIn(rating, ratings)

    def test_adminCanDeleteOtherUserRatings(self):
        self.loggedIn = self.createUserAndLogin(1, True)
        user = getUsers(2)
        book = getBooks(1)
        rating = models.BookRating.objects.create(book=book, user=user, score=1, comment="testingComment1")

        url = reverse('rating-delete', args=[rating.id])
        response = self.client.get(url)

        ratings = models.BookRating.objects.filter(book=book)

        self.assertTrue(self.loggedIn)
        self.assertEqual(ratings.count(), 0)
        self.assertNotIn(rating, ratings)

    def test_userCannotDeleteOtherUserRatings(self):
        self.loggedIn = self.createUserAndLogin(1)
        user = getUsers(2)
        book = getBooks(1)
        rating = models.BookRating.objects.create(book=book, user=user, score=1, comment="testingComment1")

        url = reverse('rating-delete', args=[rating.id])
        response = self.client.get(url)

        ratings = models.BookRating.objects.filter(book=book)

        self.assertTrue(self.loggedIn)
        self.assertEqual(ratings.count(), 1)
        self.assertIn(rating, ratings)

    def test_bookDetailPageShowsRatings(self):
        book = getBooks(1)
        user = getUsers(1)
        r1 = models.BookRating.objects.create(book=book, user=user, score=1, comment="testingComment1")
        r2 = models.BookRating.objects.create(book=book, user=user, score=2, comment="testingComment2")
        r3 = models.BookRating.objects.create(book=book, user=user, score=3, comment="testingComment3")

        url = reverse('book-detail', args=[book.id])
        response = self.client.get(url)

        self.assertEqual(list(response.context['bookRatings']), [r1, r2, r3])

