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

    def test_makeable_amount_without_components(self):
        self.assertEqual(self.product.makeable_amount, 0)

    def test_makeable_amount(self):
        self.composition1 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp1, quantity=500)
        self.composition2 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp2, quantity=200)

        expected_amount = 2000 / 500

        self.assertEqual(self.product.makeable_amount, expected_amount)

    def test_makeable_amount_with_changed_quantity(self):
        self.composition1 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp1, quantity=500)
        self.composition2 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp2, quantity=200)

        composition = ProductComposition.objects.get(
            product=self.product, subproduct=self.subp2)
        composition.quantity = 1000
        composition.save()

        old_amount = 2000 / 500
        expected_amount = 3000 / 1000

        self.assertNotEqual(self.product.makeable_amount, old_amount)
        self.assertEqual(self.product.makeable_amount, expected_amount)

    def test_price_without_components(self):
        self.assertEqual(self.product.price, 0)

    def test_price(self):
        self.composition1 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp1, quantity=500)
        self.composition2 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp2, quantity=200)

        expected_price = 500 * self.PRICE_SUBP + 200 * self.PRICE_SUBP
        self.assertEqual(self.product.price, expected_price)

    def test_price_with_changed_quantity(self):
        self.composition1 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp1, quantity=500)
        self.composition2 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp2, quantity=200)

        composition = ProductComposition.objects.get(
            product=self.product, subproduct=self.subp2)
        composition.quantity = 1000
        composition.save()

        old_price = 500 * self.PRICE_SUBP + 200 * self.PRICE_SUBP
        expected_price = 500 * self.PRICE_SUBP + 1000 * self.PRICE_SUBP

        self.assertNotEqual(self.product.price, old_price)
        self.assertEqual(self.product.price, expected_price)
