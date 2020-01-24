from rest_framework.routers import SimpleRouter
from users import views

router = SimpleRouter()

router.register(r'users', views.CustomUserViewSet)
