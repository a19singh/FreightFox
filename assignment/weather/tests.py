import json

from datetime import date
from django.test import TestCase
from django.conf import settings

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, override_settings

from .models import Location, Weather

BASE_URL = 'localhost'



class WeatherTests(APITestCase):
    """
    POC test cases for 
    Weather CRUD Operations
    """

    @override_settings(ALLOWED_HOSTS=[f'{BASE_URL}'])
    def test_successful_weather(self):
        """
        Test case for successful weather fetch
        Returns 201 created
        """
        url = reverse('get-loc-weather')
        _date = date.today()
        url += f'?date={_date}&pincode=560048'
        data_count = Weather.objects.count()
        response = self.client.get(url, SERVER_NAME=f'{BASE_URL}')
        data_count_post = Weather.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_count_post, data_count + 1)

    @override_settings(ALLOWED_HOSTS=[f'{BASE_URL}'])
    def test_invalid_datetime(self):
        """
        Testcase for invalid date format
        """
        url = reverse('get-loc-weather')
        _date = date.today().strftime("%b-%d-%Y")
        url += f'?date={_date}&pincode=560048'
        data_count = Weather.objects.count()
        response = self.client.get(url, SERVER_NAME=f'{BASE_URL}')
        data_count_post = Weather.objects.count()
        error_status = ["Please provide the date in appropriate format: YYYY-MM-DD"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), error_status)

    @override_settings(ALLOWED_HOSTS=[f'{BASE_URL}'])
    def test_invalid_pincode(self):
        """
        Testcase for invalid pincode
        """
        url = reverse('get-loc-weather')
        _date = date.today()
        url += f'?date={_date}&pincode=5600484'
        data_count = Weather.objects.count()
        response = self.client.get(url, SERVER_NAME=f'{BASE_URL}')
        data_count_post = Weather.objects.count()
        error_status = ["Invalid pincode format: max allowed length is 6"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), error_status)
