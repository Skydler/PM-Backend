from rest_framework.routers import DefaultRouter
from products.router import router as router_product

router = DefaultRouter()

router.registry.extend(router_product.registry)
