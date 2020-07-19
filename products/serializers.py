from rest_framework import serializers
from .models import Product, SubProduct, ProductComposition, Measure, PackagingObject
from .fields import UserProductsField, UserSubProductsField, UserPackagingObjectsField


class ProductCompositionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    subproduct = UserSubProductsField(view_name='subproduct-detail')
    product = UserProductsField(view_name='product-detail')

    class Meta:
        model = ProductComposition
        fields = '__all__'


class SubProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SubProduct
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    compositions = serializers.HyperlinkedRelatedField(
        view_name='productcomposition-detail', many=True, read_only=True)

    measures = serializers.HyperlinkedRelatedField(
        view_name='measure-detail', many=True, read_only=True)

    price = serializers.FloatField(read_only=True)
    makeable_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class MeasureSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    product = UserProductsField(view_name='product-detail')
    packaging_objects = UserPackagingObjectsField(
        view_name='packagingobject-detail', many=True)

    total_cost = serializers.FloatField(read_only=True)

    class Meta:
        model = Measure
        fields = '__all__'


class PackagingSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = PackagingObject
        fields = '__all__'
