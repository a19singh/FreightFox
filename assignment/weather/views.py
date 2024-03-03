import json
import logging
from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Location, Weather 
from .serializers import LocationSerializer, WeatherSerializer
from utils.api_key import openweather as apikey
from utils.rest import rest_helper as Rest

logger = logging.getLogger(__name__)

class WeatherView(APIView):
    """
    Weather View to fetch the weather for a particular pincode on a specified date. 
    """
    def get(self, request, *args, **kwargs):
        """
        Method to overwirte default functionality of get method.
        """
        weather_data = {}
        status_code = 400
        try:
            date = request.GET.get('date')
            pin = request.GET.get('pincode')
            serializer_date = WeatherSerializer(data={'date': date})
            serializer_pin = LocationSerializer(data={'pincode': pin})
            if not serializer_date.is_valid():
                raise ValidationError('Please provide the date in appropriate format: YYYY-MM-DD')
            if not serializer_pin.is_valid():
                raise ValidationError('Invalid pincode format: max allowed length is 6')
            qs = Weather.objects.filter(date=date, pincode__pincode=pin)

            # if data already present skip external api calls
            if qs:
                weather_data = json.loads(qs.first().data)
                status_code = status.HTTP_200_OK
                return Response(weather_data, status_code)

            # Calling location api to extract coordinates from pincode
            lat, long = self.__get_lat_long(pin)
            location_model_data = {'lat': lat, 'long': long, 'pincode': pin}
            # Creating and saving data in database for caching
            location_instance = Location.objects.create(**location_model_data)

            # Calling weather api for a specific coordinates
            weather_data = self.__get_weather(date, lat, long)
            weather_model_data = {'date': date, 'pincode': location_instance, 'data': json.dumps(weather_data)}
            # Creating and saving data in database for caching
            weather_instance = Weather.objects.create(**weather_model_data)
            status_code = status.HTTP_200_OK
            return Response(weather_data, status_code)

        except ValidationError as e:
            return Response(e.detail, status_code)

        except:
            return Response(weather_data, status_code)

    def __get_lat_long(self, pincode, country="IN"):
        """
        Method to extract latitude and longitude for a pincode.
        """
        url = f'https://api.openweathermap.org/geo/1.0/zip'
        params = {
                "zip": f"{pincode},{country}",
                "appid": f"{apikey}"
        }
        response = Rest(url, params=params)
        return response.get('lat'), response.get('lon')

    def __get_weather(self, date, lat, lon):
        """
        Method to extract weather info for given lattitud and longitude
        """
        # Using current data api as historical data api was paid
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
                "lat": f"{lat}",
                "lon": f"{lon}",
                "appid": f"{apikey}"
        }
        response = Rest(url, params=params)
        return response

