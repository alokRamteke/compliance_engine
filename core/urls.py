from django.urls import include, path
from rest_framework import routers

from core.views import (ContentDetailView, ContentListView,
                        ContentReviewStatusView, ContentReviewUpdateView,
                        ContentUploadView, GuidelineViewSet)

router = routers.SimpleRouter()
router.register(r'guidelines', GuidelineViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/content/', ContentListView.as_view(), name='content-list'),
    path('v1/content/upload/', ContentUploadView.as_view(), name='content-upload'),
    path('v1/content/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
    path(
        'v1/content/<int:content_id>/review-status/',
        ContentReviewStatusView.as_view(),
        name='content-review-status',
    ),
    path(
        'v1/content/<int:content_id>/review/<int:review_item_id>/',
        ContentReviewUpdateView.as_view(),
        name='content-review-update',
    ),
]
