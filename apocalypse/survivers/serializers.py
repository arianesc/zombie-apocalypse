from rest_framework import serializers
from survivers.models import Surviver


class SurviverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surviver
        fields = ('id', 'name', 'age', 'gender', 'latitude', 'longitude', 'food', 'water', 'medication', 'ammunition', 'infected')

    def create(self, validated_data):
        """
        Create and return a new `Surviver` instance
        """
        return Surviver.objects.create(**validated_data)