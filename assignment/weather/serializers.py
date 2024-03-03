import logging
from rest_framework import serializers

from .models import Location, Weather 

logger = logging.getLogger(__name__)

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer to validate location models values.
    """
    class Meta:
        model = Location
        fields = ['pincode']


class WeatherSerializer(serializers.ModelSerializer):
    """
    Serializer to validate location models values.
    """
    class Meta:
        model = Weather
        fields = ['date']
