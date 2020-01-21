from django.test import TestCase
from users.models import CustomUser
from products.models import Product, SubProduct


class SubProductTest(TestCase):

    @classmethod
    def setUpTestData(self):
        user = CustomUser.objects.create(
            username='Pepe', password='omegalul123')

        self.subproduct = SubProduct.objects.create(
            name='Keratina', owner=user, current_amount=500, price=0.5)

        self.product = Product.objects.create(name='Splash', owner=user)
        self.product.components.add(
            self.subproduct, through_defaults={'quantity': 100})

    def test_calculate_units_for_product(self):
        units = self.subproduct.calculate_units_for_product(self.product)
        self.assertEqual(units, 5)

    def test_calculate_price_with_quantity(self):
        price = self.subproduct.calculate_price_with_quantity(self.product)
        expected = 0.5 * 100
        self.assertEqual(price, expected)

    def test_get_quantity_for_product(self):
        quantity = self.subproduct.get_quantity_for_product(self.product)
        self.assertEqual(quantity, 100)
