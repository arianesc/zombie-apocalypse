from rest_framework import serializers
from survivers.models import Surviver


class SurviverSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    age = serializers.PositiveIntegerField(required=True, allow_blank=False)
    gender = serializers.CharField(required=True, allow_blank=False, max_length=10)
    latitude = serializers.CharField(required=True, allow_blank=False, max_length=100)
    longitude = serializers.CharField(required=True, allow_blank=False, max_length=100)
