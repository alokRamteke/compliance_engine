from rest_framework import serializers
from core.models import Guideline, Content


class GuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guideline
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ('title', 'file')
