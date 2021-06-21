from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Product,
    ProductComposition,
    SalesRecord,
    SubProduct,
    Measure,
    PackagingObject,
)
from .serializers import (
    ProductSerializer,
    ProductCompositionSerializer,
    SalesSerializer,
    SubProductSerializer,
    MeasureSerializer,
    PackagingSerializer,
)
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

    @action(detail=True)
    def components_data(self, request, pk=None):
        product = self.get_object()
        subproducts = [comp.subproduct for comp in product.compositions.all()]
        not_used_subproduct_objs = SubProduct.objects.exclude(
            id__in=[subp.id for subp in subproducts]
        )

        compositions = ProductCompositionSerializer(
            product.compositions, many=True, context={"request": request}
        )
        usedSubproducts = SubProductSerializer(
            subproducts, many=True, context={"request": request}
        )
        notUsedSubproducts = SubProductSerializer(
            not_used_subproduct_objs, many=True, context={"request": request}
        )
        packaging = PackagingSerializer(
            PackagingObject.objects.all(), many=True, context={"request": request}
        )
        measures = MeasureSerializer(
            product.measures, many=True, context={"request": request}
        )

        components_data = {
            "compositions": compositions.data,
            "usedSubproducts": usedSubproducts.data,
            "notUsedSubproducts": notUsedSubproducts.data,
            "packagingObjects": packaging.data,
            "measures": measures.data,
        }
        return Response(components_data)


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


class SalesViewSet(viewsets.ModelViewSet):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        user_objs = queryset.filter(owner=self.request.user)
        return user_objs
