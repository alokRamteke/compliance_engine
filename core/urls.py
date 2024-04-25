from django.urls import path, include
from rest_framework import routers
from core.views import GuidelineViewSet

router = routers.SimpleRouter()
router.register(r'guidelines', GuidelineViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
