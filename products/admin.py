from django.contrib import admin
from .models import (
    Product,
    ProductComposition,
    Measure,
    SubProduct,
    PackagingObject,
    SalesRecord,
)


class SubProductAdmin(admin.ModelAdmin):
    list_display = ("name", "current_amount", "price", "owner")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "current_amount", "cost", "owner")


class ProductCompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "subproduct", "quantity")


class MeasureAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "size", "price", "product", "total_cost")


class PackagingObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "current_amount", "price", "owner")


class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "product_sold", "liters_sold", "price")


admin.site.register(SubProduct, SubProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComposition, ProductCompositionAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(PackagingObject, PackagingObjectAdmin)
admin.site.register(SalesRecord, SalesRecordAdmin)
