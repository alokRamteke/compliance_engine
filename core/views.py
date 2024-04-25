from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Content, Guideline, ReviewItem
from core.serializers import (ContentSerializer, GuidelineSerializer,
                              ReviewItemSerializer)


class GuidelineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Guideline model. Provides basic CRUD operations via HTTP.
    """
    queryset = Guideline.objects.all()
    serializer_class = GuidelineSerializer
    http_method_names = ('get', 'patch', 'post', 'put')


class ContentListView(generics.ListAPIView):
    """
    ListView for the Content model. It provides a GET request to retrieve all instances of Content.
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentUploadView(generics.CreateAPIView):
    """
    API View to handle uploading of new content.
    """
    serializer_class = ContentSerializer
    parser_classes = [MultiPartParser, FileUploadParser]

    def create(self, request, *args, **kwargs):
        """
        Create a new Content instance using the provided data.
        """
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            # Check if a content with the same title already exists for the user
            existing_content = Content.objects.filter(
                author=user, title=request.data['title']
            )
            if existing_content.exists():
                error_message = (
                    'Content with the same title already exists. '
                    'Please choose a unique title or update existing content.'
                )
                return Response(
                    {'error': error_message},
                    status=status.HTTP_409_CONFLICT,
                )
            serializer.validated_data['author'] = user
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(generics.RetrieveUpdateAPIView):
    """
    API View to handle retrieval and updating of a Content instance.
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def patch(self, request, *args, **kwargs):
        """
        Update a Content instance if it belongs to the requesting user.
        """
        content = self.get_object()
        if content.author != request.user:
            return Response(
                {'error': 'You can only update content you own.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        updated_content = request.data.get('file')
        serializer = self.get_serializer(content, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if updated_content is not None:
            serializer.validated_data['version'] = content.version + 1

        self.perform_update(serializer)

        return Response(serializer.data)


class ContentReviewStatusView(APIView):
    """
    API View to check the status of review items for a specific content.
    """
    def get(self, request, content_id):
        """
        Retrieves status of review items for a specific content.
        """
        try:
            content = Content.objects.get(pk=content_id)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reviews = ReviewItem.objects.filter(content=content)
        review_items = ReviewItemSerializer(reviews, many=True).data

        return Response(review_items)


class ContentReviewUpdateView(generics.UpdateAPIView):
    """
    API View to update a ReviewItem instance for a specific content.
    """
    serializer_class = ReviewItemSerializer
    queryset = ReviewItem.objects.all()

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
        Update a ReviewItem instance if it belongs to the specified content.
        """
        content_id = self.kwargs.get('content_id')
        review_item_id = self.kwargs.get('review_item_id')

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response(
                {'error': 'No Content matches the given query.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        review_item = content.review_items.filter(pk=review_item_id).first()
        if not review_item:
            return Response(
                {'error': 'No Review item matches the given query.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(review_item, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        review_item.reviewer = request.user
        review_item.reviewed_at = timezone.now()
        review_item.save()

        return Response(serializer.data)
