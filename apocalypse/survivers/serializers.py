from rest_framework import serializers
from survivers.models import Surviver


class SurviverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surviver
        fields = ('id', 'name', 'age', 'gender', 'latitude', 'longitude',
                  'food', 'water', 'medication', 'ammunition', 'infected')