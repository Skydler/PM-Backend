from django.test import TestCase
from users.models import CustomUser
from products.models import Product, SubProduct, PackagingObject, Measure, ProductComposition


class MeasureTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = CustomUser.objects.create(
            username='Pepe', password='omegalul123')

        self.create_subproducts()
        self.create_product()
        self.create_packaging()
        self.create_measure()

    @classmethod
    def create_subproducts(self):
        self.subp1 = SubProduct.objects.create(
            name='Keratina', owner=self.user, current_amount=2000, price=10)
        self.subp2 = SubProduct.objects.create(
            name='Formol', owner=self.user, current_amount=3000, price=20)

    @classmethod
    def create_product(self):
        self.product = Product.objects.create(
            name='Brasilero', owner=self.user)

        self.composition1 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp1, quantity=500)
        self.composition2 = ProductComposition.objects.create(
            product=self.product, subproduct=self.subp2, quantity=200)

    @classmethod
    def create_packaging(self):
        self.pack1 = PackagingObject.objects.create(
            name='Etiqueta', owner=self.user, current_amount=10, price=40)
        self.pack2 = PackagingObject.objects.create(
            name='Envase medio litro', owner=self.user, current_amount=20, price=70)

    @classmethod
    def create_measure(self):
        self.measure = Measure.objects.create(
            name='Medio Litro', size=0.5, price=400, product=self.product)

        self.measure.packaging_objects.add(self.pack1, self.pack2)

    def test_total_cost(self):
        product_cost = self.product.price * self.measure.size
        packaging_cost = 40 + 70
        total_cost = product_cost + packaging_cost

        self.assertEqual(self.measure.total_cost, total_cost)
