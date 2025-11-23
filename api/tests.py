from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Category, Material, Product, CustomOrder, ContactMessage, Newsletter


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )
        self.material = Material.objects.create(
            name="PLA",
            description="Test material"
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test description",
            price=999,
            category=self.category,
            material=self.material,
            stock_quantity=10,
            is_available=True
        )

    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_product_detail(self):
        response = self.client.get(f'/api/products/{self.product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_filter_products_by_category(self):
        response = self.client.get(f'/api/products/?category__slug={self.category.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class CustomOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_custom_order(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+91 1234567890',
            'material': 'PLA',
            'color': 'Blue',
            'description': 'Test order',
            'quantity': 1
        }
        response = self.client.post('/api/custom-orders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_create_custom_order_missing_fields(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com'
            # Missing required fields
        }
        response = self.client.post('/api/custom-orders/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ContactMessageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_contact_message(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        }
        response = self.client.post('/api/contact/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class NewsletterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_newsletter_subscription(self):
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/newsletter/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_newsletter_subscription(self):
        Newsletter.objects.create(email='test@example.com')
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/newsletter/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
