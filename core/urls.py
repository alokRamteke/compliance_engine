from django.urls import path, include
from rest_framework import routers
from core.views import GuidelineViewSet, ContentUploadView, ContentDetailView

router = routers.SimpleRouter()
router.register(r'guidelines', GuidelineViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/content/upload/', ContentUploadView.as_view(), name='content-upload'),
    path('v1/content/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
]
