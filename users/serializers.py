from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser

        fields = ['url', 'username', 'is_staff',
                  'product_set', 'subproduct_set', 'packagingobject_set', ]
