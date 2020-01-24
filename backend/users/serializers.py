from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'product_set', 'subproduct_set', 'packagingobject_set', ]
