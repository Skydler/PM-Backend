from django.test import TestCase
from users.models import CustomUser
from products.models import Product, SubProduct, ProductComposition


class ProductTest(TestCase):
    PRICE_SUBP = 1

    @classmethod
    def setUpTestData(self):
        user = CustomUser.objects.create(
            username='Pepe', password='omegalul123')

        self.subp1 = SubProduct.objects.create(
            name='Keratina', owner=user, current_amount=2000, price=self.PRICE_SUBP)
        self.subp2 = SubProduct.objects.create(
            name='Formol', owner=user, current_amount=3000, price=self.PRICE_SUBP)

        self.product = Product.objects.create(name='Marroqui', owner=user)

    def test_makeable_amount(self):
        self.assertIsNone(self.product.makeable_amount)

        self.product.components.add(
            self.subp1, through_defaults={'quantity': 500})
        self.product.components.add(
            self.subp2, through_defaults={'quantity': 200})

        expected_amount = 2000 / 500
        self.assertEqual(self.product.makeable_amount, 4)

        composition = ProductComposition.objects.get(
            product=self.product, subproduct=self.subp2)
        composition.quantity = 1000
        composition.save()

        mod_expected_amount = 3000 / 1000
        self.assertNotEqual(self.product.makeable_amount, expected_amount)
        self.assertEqual(self.product.makeable_amount, mod_expected_amount)

    def test_production_cost_liter(self):
        self.assertIsNone(self.product.production_cost_liter)

        self.product.components.add(
            self.subp1, through_defaults={'quantity': 500})
        self.product.components.add(
            self.subp2, through_defaults={'quantity': 200})

        expected_price = 500 * self.PRICE_SUBP + 200 * self.PRICE_SUBP
        self.assertEqual(self.product.production_cost_liter, expected_price)

        composition = ProductComposition.objects.get(
            product=self.product, subproduct=self.subp2)
        composition.quantity = 1000
        composition.save()

        mod_expected_price = 500 * self.PRICE_SUBP + 1000 * self.PRICE_SUBP
        self.assertNotEqual(self.product.production_cost_liter, expected_price)
        self.assertEqual(self.product.production_cost_liter, mod_expected_price)
