from rest_framework.routers import SimpleRouter
from products import views

router = SimpleRouter()

router.register(r'products', views.ProductViewSet)
router.register(r'subproducts', views.SubProductViewSet)
router.register(r'compositions', views.ProductCompositionViewSet)
router.register(r'measures', views.MeasureViewSet)
router.register(r'packaging', views.PackagingViewSet)
