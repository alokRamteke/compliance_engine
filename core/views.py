from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Guideline, Content, ReviewItem
from core.serializers import GuidelineSerializer, ContentSerializer, ReviewItemSerializer
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.db import transaction


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


class ContentReviewStatusView(APIView):

    def get(self, request, content_id):
        try:
            content = Content.objects.get(pk=content_id)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reviews = ReviewItem.objects.filter(content=content)
        review_items = ReviewItemSerializer(reviews, many=True).data

        return Response(review_items)


class ContentReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewItemSerializer
    queryset = ReviewItem.objects.all()

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        content_id = self.kwargs.get('content_id')
        review_item_id = self.kwargs.get('review_item_id')

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({'error': 'No Content matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

        review_item = content.review_items.filter(pk=review_item_id).first()
        if not review_item:
            return Response({'error': 'No Review item matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = self.get_serializer(review_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        review_item.reviewer = request.user
        review_item.reviewed_at = timezone.now()
        review_item.save()

        return Response(serializer.data)
