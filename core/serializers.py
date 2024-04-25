from rest_framework import serializers
from core.models import Guideline, Content, ReviewItem
from django.core.exceptions import ValidationError
from os.path import splitext

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".docx", ".txt", ".pdf"]


class GuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guideline
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        read_only_fields = ('id', 'version', 'author')
        fields = (*read_only_fields, 'title', 'file')
    
    def validate_file(self, file):
        _, extension = splitext(file.name)
        extension = extension.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError('Invalid file type. Only images, Word documents, TXT, and PDF files are allowed.')
        return file


class ReviewItemSerializer(serializers.ModelSerializer):
    guideline = GuidelineSerializer(read_only=True)
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = ReviewItem
        fields = ('id', 'guideline', 'status', 'reviewer')

    def get_reviewer(self, obj):
        if obj.reviewer:
            return obj.reviewer.get_full_name()
        else:
            return None
