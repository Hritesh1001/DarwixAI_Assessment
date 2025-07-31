# blog/serializers.py
from rest_framework import serializers

class TitleRequestSerializer(serializers.Serializer):
    content = serializers.CharField()

class TitleResponseSerializer(serializers.Serializer):
    titles = serializers.ListField(
        child=serializers.CharField(), min_length=1
    )
