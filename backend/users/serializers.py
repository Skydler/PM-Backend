from rest_framework import serializers
from products.models import Product
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'products', ]
