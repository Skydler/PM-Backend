from django.test import TestCase
from users.models import CustomUser
from products.models import SubProduct


class SubProductTest(TestCase):

    @classmethod
    def setUpTestData(self):
        user = CustomUser.objects.create(
            username='Pepe', password='omegalul123')

        self.subproduct = SubProduct.objects.create(
            name='Keratina', owner=user, current_amount=500, price=0.5)
        self.amount = 100

    def test_calculate_units_for_amount(self):
        units = self.subproduct.calculate_units_for_amount(self.amount)
        self.assertEqual(units, 5)

    def test_calculate_price_for_amount(self):
        price = self.subproduct.calculate_price_for_amount(self.amount)
        expected = 0.5 * 100
        self.assertEqual(price, expected)
