from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
        path('', views.WeatherView.as_view(), name='get-loc-weather'),
        # path('', views.WeatherView.as_view({'get': 'list'}), name='get-loc-weather'),
]
