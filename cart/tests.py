from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Category, SubCategory, Product

User = get_user_model()


class CartAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(self.user)
        c = Category.objects.create(name='Cat', slug='cat')
        sc = SubCategory.objects.create(category=c, name='Sub', slug='sub')
        self.product = Product.objects.create(category=c, subcategory=sc, name='P', slug='p', price=5.0)

    def test_add_to_cart(self):
        resp = self.client.post('/api/cart/add/', {'product': self.product.id, 'quantity': 2}, format='json')
        self.assertEqual(resp.status_code, 201)
        resp2 = self.client.get('/api/cart/')     # check cart detail
        self.assertEqual(resp2.status_code, 200)
        data = resp2.json()
        self.assertEqual(data['total_quantity'], 2)
