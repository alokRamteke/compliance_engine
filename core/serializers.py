from os.path import splitext

from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.constants import ALLOWED_EXTENSIONS
from core.models import Content, Guideline, ReviewItem


class GuidelineSerializer(serializers.ModelSerializer):
    """
    Serializer for Guideline model.
    """
    class Meta:
        model = Guideline
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for Content model.
    """
    review_status = serializers.SerializerMethodField()

    class Meta:
        model = Content
        read_only_fields = (
            'id',
            'version',
            'author',
            'created_at',
            'updated_at',
            'review_status',
        )
        fields = (*read_only_fields, 'title', 'file')

    def validate_file(self, file):
        """
        Validates the file extension of the uploaded file.
        """
        _, extension = splitext(file.name)
        extension = extension.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                'Invalid file type. Only images, Word documents, TXT, and PDF files are allowed.'
            )
        return file

    def get_review_status(self, obj):
        """
        Retrieves the review status of the Content object.
        """
        return obj.review_status


class ReviewItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ReviewItem model.
    """
    guideline = GuidelineSerializer(read_only=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('PASS', 'Passed'),
        ('FAIL', 'Failed'),
    ]
    status = serializers.ChoiceField(choices=status_choices)
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = ReviewItem
        fields = ('id', 'guideline', 'status', 'reviewer', 'reviewed_at')

    def get_reviewer(self, obj):
        """
        Return the full name of the reviewer, or None if reviewer is None.
        """
        if obj.reviewer:
            return obj.reviewer.get_full_name()
        else:
            return None
