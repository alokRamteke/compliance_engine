from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from core.models import Guideline, Content
from core.serializers import GuidelineSerializer, ContentSerializer
from rest_framework.parsers import MultiPartParser, FileUploadParser


class GuidelineViewSet(viewsets.ModelViewSet):
    queryset = Guideline.objects.all()
    serializer_class = GuidelineSerializer
    http_method_names = ('get', 'patch', 'post', 'put')


class ContentListView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentUploadView(generics.CreateAPIView):
    serializer_class = ContentSerializer
    parser_classes = [MultiPartParser, FileUploadParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            existing_content = Content.objects.filter(author=user, title=request.data['title'])
            if existing_content.exists():
                return Response({'error': 'Content with the same title already exists. Please choose a unique title or update existing content.'}, status=status.HTTP_409_CONFLICT)
            serializer.validated_data['author'] = user 
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def patch(self, request, *args, **kwargs):
        content = self.get_object()
        if content.author != request.user:
            return Response({'error': 'You can only update content you own.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(content, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['version'] = content.version + 1
        self.perform_update(serializer)
        return Response(serializer.data)
