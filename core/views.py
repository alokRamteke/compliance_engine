from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from core.models import Guideline
from core.serializers import GuidelineSerializer, ContentSerializer


class GuidelineViewSet(viewsets.ModelViewSet):
    queryset = Guideline.objects.all()
    serializer_class = GuidelineSerializer
    http_method_names = ('get', 'patch', 'post', 'put')


class ContentUploadView(generics.CreateAPIView):
    serializer_class = ContentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            serializer.validated_data['author'] = user 
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
