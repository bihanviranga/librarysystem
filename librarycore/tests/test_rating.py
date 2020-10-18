from django.test import tag
from django.test.utils import setup_test_environment
from .libraryTestCase import LibraryTestCase

@tag('rating', 'rating-crud')
class RatingViewCrudTest(LibraryTestCase):
    def setup(self):
        setup_test_environment()

    def test_createRatingPostRequest(self):
        self.fail()

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

