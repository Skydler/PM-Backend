from django.db import models
from users.models import CustomUser
# from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    current_amount = models.FloatField(default=0)

    components = models.ManyToManyField(
        'self', symmetrical=False, related_name='compose', blank=True, through='ProductComposition')
    owner = models.ForeignKey(
        CustomUser, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def input_amount(self):
        """
        Calculates the amount of product makeable with the existent subproducts.
        If this function is called from a input product returns the current_amount
        """
        components = self.get_components()
        if components:
            subproducts_makeable_amount = map(
                self._calculate_product_makeable_quantity, components)
            product_amount = min(subproducts_makeable_amount)
            return product_amount

        return self.current_amount

    def _calculate_product_makeable_quantity(self, subproduct):
        relation = subproduct.productcomposition_set.get(product=self)

        needed_amount = relation.quantity
        existent_amount = subproduct.current_amount

        return existent_amount / needed_amount

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
    product = models.ForeignKey(Product, related_name='composed_products', on_delete=models.CASCADE)
    subproduct = models.ForeignKey(Product, related_name='subproducts', on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f'Product Composition: {self.id}'


class Measure(models.Model):
    name = models.CharField(max_length=30)
    size = models.FloatField()
    price = models.FloatField()

    product = models.ForeignKey(
        Product, related_name='measures', on_delete=models.CASCADE)

    def __str__(self):
        return f'Measure: {self.name} - {self.product.name}'

    @property
    def production_cost(self):
        components = self.product.get_components()
        if components:
            components_values = map(self._get_component_prod_cost, components)
            return sum(components_values)
        return self.price

    def _get_component_prod_cost(self, component):
        # Asumo que el componente tiene una medida igual a del producto final
        measure = component.measures.get(size=self.size)
        return measure.production_cost

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'], name='unique_size_for_product')
        ]
