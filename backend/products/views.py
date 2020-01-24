from rest_framework import viewsets, permissions
from .models import Product, ProductComposition, SubProduct, Measure, PackagingObject
from .serializers import (ProductSerializer, ProductCompositionSerializer,
                          SubProductSerializer, MeasureSerializer, PackagingSerializer)
from .permissions import IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubProductViewSet(viewsets.ModelViewSet):
    queryset = SubProduct.objects.all()
    serializer_class = SubProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductCompositionViewSet(viewsets.ModelViewSet):
    queryset = ProductComposition.objects.all()
    serializer_class = ProductCompositionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class PackagingViewSet(viewsets.ModelViewSet):
    queryset = PackagingObject.objects.all()
    serializer_class = PackagingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
