from rest_framework import serializers
from core.models import Guideline, Content
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
        fields = ('title', 'file')
    
    def validate_file(self, file):
        _, extension = splitext(file.name)
        extension = extension.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError('Invalid file type. Only images, Word documents, TXT, and PDF files are allowed.')
        return file
