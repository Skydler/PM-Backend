from rest_framework import viewsets, permissions
from .models import Product, ProductComposition, SubProduct, Measure, PackagingObject
from .serializers import (ProductSerializer, ProductCompositionSerializer,
                          SubProductSerializer, MeasureSerializer, PackagingSerializer)
from .permissions import IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        user_objs = queryset.filter(owner=self.request.user)
        return user_objs


class SubProductViewSet(viewsets.ModelViewSet):
    queryset = SubProduct.objects.all()
    serializer_class = SubProductSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        user_objs = queryset.filter(owner=self.request.user)
        return user_objs


class ProductCompositionViewSet(viewsets.ModelViewSet):
    queryset = ProductComposition.objects.all()
    serializer_class = ProductCompositionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def filter_queryset(self, queryset):
        user_prods = self.request.user.product_set.all()
        user_compositions = queryset.filter(product__in=user_prods)
        return user_compositions


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def filter_queryset(self, queryset):
        user_prods = self.request.user.product_set.all()
        user_measures = queryset.filter(product__in=user_prods)
        return user_measures


class PackagingViewSet(viewsets.ModelViewSet):
    queryset = PackagingObject.objects.all()
    serializer_class = PackagingSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        user_objs = queryset.filter(owner=self.request.user)
        return user_objs
