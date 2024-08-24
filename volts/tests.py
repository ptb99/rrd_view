from django.test import TestCase
#from django.test import Client
from django.urls import reverse

# Create your tests here.
class BasicViewTests(TestCase):
    def test_index_view(self):
        """
        Checks that index page is being rendered.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        # ultimately, we should load init-data.json
        graphs = response.context['graphs']
        self.assertTrue(len(response.context) > 0)
        self.assertIsNotNone(graphs)
        self.assertEqual(len(graphs), 0)

    def test_about_view(self):
        """
        Check the about page.
        """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
