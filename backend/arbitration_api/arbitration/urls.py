from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArbitrationCaseViewSet

router = DefaultRouter()
router.register(r'cases', ArbitrationCaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
