from django.db import models
from users.models import CustomUser
# from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)

    quantity = models.FloatField()
    base_price = models.FloatField(null=True, blank=True)
    aditional_cost = models.FloatField(null=True, blank=True)

    composition = models.ManyToManyField(
        'self', symmetrical=False, related_name='compose', blank=True)

    owner = models.ForeignKey(
        CustomUser, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('product', args=[str(self.pk)])
