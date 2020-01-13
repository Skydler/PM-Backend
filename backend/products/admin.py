from django.contrib import admin
from .models import Product, ProductComposition, Measure


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_amount',)


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'size', 'price', 'product',)


class ProductCompositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'subproduct', 'quantity',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComposition, ProductCompositionAdmin)
admin.site.register(Measure, MeasureAdmin)
