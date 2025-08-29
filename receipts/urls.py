from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReceiptViewSet, RecommendationView

router = DefaultRouter()
router.register(r"receipts", ReceiptViewSet, basename="receipt")

urlpatterns = [
    path("", include(router.urls)),
    path("recommendations/", RecommendationView.as_view(), name="recommendations"),
]
