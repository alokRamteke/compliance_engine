from rest_framework import viewsets
from core.models import Guideline
from core.serializers import GuidelineSerializer


class GuidelineViewSet(viewsets.ModelViewSet):
    queryset = Guideline.objects.all()
    serializer_class = GuidelineSerializer
    http_method_names = ('get', 'patch', 'post', 'put')
