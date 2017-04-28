from rest_framework import serializers

from ..serializers import ModelSerializer
from .models import Page


class PageSerializer(ModelSerializer):

    class Meta:
        model = Page
        fields = '__all__'

    path = serializers.CharField()
