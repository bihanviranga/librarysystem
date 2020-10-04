from django.test import tag, TestCase
from django.test.utils import setup_test_environment
from django.urls import reverse

@tag('general')
class GeneralSiteTests(TestCase):
    def setup(self):
        setup_test_environment()

    def test_indexHasCurrentNavSet(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.context['currentNav'], 'index')

