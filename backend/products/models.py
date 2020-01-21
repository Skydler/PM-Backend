from django.db import models
from users.models import CustomUser
# from django.urls import reverse


class BaseProduct(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    current_amount = models.FloatField(
        default=0, help_text='amount in milliliters')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SubProduct(BaseProduct):
    price = models.FloatField(help_text='Price of a milliliter of the product')

    def calculate_units_for_product(self, product):
        """
        Calculates how many units of a product are makeable with the existent subproduct
        """
        needed_amount = self.get_quantity_for_product(product)
        return self.current_amount / needed_amount

    def calculate_price_with_quantity(self, product):
        """
        Calculates the price of the subproduct considering the quantity that composes a product
        """
        quantity = self.get_quantity_for_product(product)
        return quantity * self.price

    def get_quantity_for_product(self, product):
        composition = self.productcomposition_set.get(product=product)
        return composition.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_subproduct_for_user')
        ]


class Product(BaseProduct):
    components = models.ManyToManyField(
        SubProduct, blank=True, through='ProductComposition')

    @property
    def makeable_amount(self):
        """
        Calculates the amount of product makeable with the existent subproducts.
        """
        components = self.get_components()
        if components:
            subproducts_makeable_amounts = map(
                lambda comp: comp.calculate_units_for_product(self), components)
            product_amount = min(subproducts_makeable_amounts)
            return product_amount

    @property
    def production_cost_liter(self):
        """
        Calculates the price of a liter of the product
        """
        components = self.get_components()
        if components:
            components_prices = map(
                lambda comp: comp.calculate_price_with_quantity(self), components)
            price = sum(components_prices)
            return price

    def get_components(self):
        return self.components.all()

    # def get_absolute_url(self):
    #     return reverse('product', args=[str(self.pk)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_product_for_user')
        ]


class ProductComposition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subproduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE)

    quantity = models.FloatField(help_text='quantity in milliliters')

    def __str__(self):
        return f'Product Composition: {self.id}'


class Measure(models.Model):
    name = models.CharField(max_length=30)
    size = models.FloatField(help_text='size in liters')
    price = models.FloatField(help_text='selling price')

    product = models.ForeignKey(
        Product, related_name='measures', on_delete=models.CASCADE)

    def __str__(self):
        return f'Measure: {self.name} - {self.product.name}'

    @property
    def total_cost(self):
        product_cost = self.product.production_cost_liter * self.size
        packaging_cost = sum(
            map(lambda obj: obj.price, self.packaging_objects.all()))
        return product_cost + packaging_cost

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'], name='unique_size_for_product')
        ]


class PackagingObject(BaseProduct):
    current_amount = models.IntegerField()
    price = models.FloatField()

    measure = models.ForeignKey(
        Measure, related_name='packaging_objects', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_packaging_for_user')
        ]
