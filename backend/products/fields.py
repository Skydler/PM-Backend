from rest_framework import serializers
from .models import Product, SubProduct, PackagingObject


class UserSubProductsField(serializers.HyperlinkedRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        filtered_subproducts = SubProduct.objects.filter(owner=current_user)
        return filtered_subproducts


class UserProductsField(serializers.HyperlinkedRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        filtered_products = Product.objects.filter(owner=current_user)
        return filtered_products


class UserPackagingObjectsField(serializers.HyperlinkedRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        filtered_products = PackagingObject.objects.filter(owner=current_user)
        return filtered_products
