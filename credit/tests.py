from django.test import TestCase, Client
from .models import Customer, Product, Installment
from .views import ProductListView, ProductDetailView, InstallmentView, InstallmentSuccessView

class ProductListViewTest(TestCase):

    def setUp(self):
        Product.objects.create(name="Laptop", price=50000)
        Product.objects.create(name="Phone", price=20000)
        Product.objects.create(name="TV", price=30000)

    def test_product_list_view(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "50000")
        self.assertContains(response, "Phone")
        self.assertContains(response, "20000")
        self.assertContains(response, "TV")
        self.assertContains(response, "30000")

class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price=50000)

    def test_product_detail_view(self):
        client = Client()
        response = client.get(f"/product/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "50000")

class InstallmentViewTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price=50000)
        self.customer = Customer.objects.create(first_name="Alice", last_name="Smith", phone_number="1234567890")

    def test_installment_view_get(self):
        client = Client()
        response = client.get(f"/product/{self.product.id}/installment/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "Phone number")
        self.assertContains(response, "Term")

    def test_installment_view_post_success(self):
        client = Client()
        response = client.post(f"/product/{self.product.id}/installment/", {
             "first_name": "Alice",
             "last_name": "Smith",
             "phone_number": "1234567890",
             "term": "4",
        })