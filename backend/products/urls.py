from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'subproducts', views.SubProductViewSet)
router.register(r'compositions', views.ProductCompositionViewSet)
router.register(r'measures', views.MeasureViewSet)
router.register(r'packaging', views.PackagingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
