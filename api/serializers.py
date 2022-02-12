"""api serializers"""

from rest_framework import serializers
from api import models


class PetsPhotoSerializer(serializers.Serializer):
    # pet photo serializer
    file = serializers.ImageField()


class DeletePetsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField())


class PetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pets
        fields = ("id", "name", "type", "created_at", "photos", "age")
