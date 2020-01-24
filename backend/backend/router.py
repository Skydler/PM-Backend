from rest_framework.routers import DefaultRouter
from products.router import router as router_product
from users.router import router as router_users

router = DefaultRouter()

router.registry.extend(router_product.registry)
router.registry.extend(router_users.registry)
