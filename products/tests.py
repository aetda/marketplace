from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from products.models import Category


class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Category.objects.create(name='TestCat', slug='testcat')

    def test_get_categories(self):
        resp = self.client.get('/api/products/categories/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('results', data)
        self.assertTrue(len(data['results']) >= 1)
