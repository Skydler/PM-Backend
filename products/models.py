from django.db import models
from users.models import CustomUser
from django.urls import reverse


class BaseProduct(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    current_amount = models.FloatField(
        default=0, help_text='Amount in milliliters')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SubProduct(BaseProduct):
    price = models.FloatField(help_text='Price of a milliliter of the product')

    def calculate_units_for_amount(self, amount):
        # TODO Need to restrict this to milliliters input
        return self.current_amount / amount

    def calculate_price_for_amount(self, amount):
        # TODO Need to restrict this to milliliters input
        return self.price * amount

    def get_absolute_url(self):
        return reverse('subproducts', args=[str(self.pk)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_subproduct_for_user')
        ]


class Product(BaseProduct):

    @property
    def makeable_amount(self):
        """
        Calculates the amount of product makeable with the existent subproducts.
        """
        compositions = self.get_compositions()
        if compositions:
            subproducts_makeable_amounts = map(
                lambda comp: comp.calculate_units_of_subproduct(), compositions)
            product_amount = min(subproducts_makeable_amounts)
            return product_amount
        return 0

    @property
    def production_cost_liter(self):
        """
        Calculates the price of a liter of product
        """
        compositions = self.get_compositions()
        if compositions:
            components_prices = map(
                lambda comp: comp.get_cost(), compositions)
            price = sum(components_prices)
            return price
        return 0

    def get_compositions(self):
        return self.compositions.all()

    def get_absolute_url(self):
        return reverse('products', args=[str(self.pk)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_product_for_user')
        ]


class ProductComposition(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='compositions')
    subproduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE)

    quantity = models.FloatField(help_text='Quantity in milliliters')

    def calculate_units_of_subproduct(self):
        return self.subproduct.calculate_units_for_amount(self.quantity)

    def get_cost(self):
        return self.subproduct.calculate_price_for_amount(self.quantity)

    def __str__(self):
        return f'Product Composition: {self.id}'

    def get_absolute_url(self):
        return reverse('compositions', args=[str(self.pk)])


class Measure(models.Model):
    name = models.CharField(max_length=30)
    size = models.FloatField(help_text='Size in liters')
    price = models.FloatField(help_text='Selling price')

    product = models.ForeignKey(
        Product, related_name='measures', on_delete=models.CASCADE)

    packaging_objects = models.ManyToManyField('PackagingObject', blank=True)

    def __str__(self):
        return f'Measure: {self.name} - {self.product.name}'

    @property
    def total_cost(self):
        product_cost = self.product.production_cost_liter * self.size
        packaging_cost = self.calculate_packaging_cost()
        return product_cost + packaging_cost

    def calculate_packaging_cost(self):
        packaing_prices = map(lambda obj: obj.price, self.packaging_objects.all())
        packaging_cost = sum(packaing_prices)
        return packaging_cost

    def get_absolute_url(self):
        return reverse('measures', args=[str(self.pk)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'], name='unique_size_for_product')
        ]


class PackagingObject(BaseProduct):
    current_amount = models.IntegerField()
    price = models.FloatField()

    def get_absolute_url(self):
        return reverse('packaging', args=[str(self.pk)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], name='unique_packaging_for_user')
        ]
