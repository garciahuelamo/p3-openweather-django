from django.urls import path
from .views import WeatherOverviewView

urlpatterns = [
    path("api/weather/", WeatherOverviewView.as_view(), name="weather_overview"),
    path('api/weather/<int:weather_id>/', WeatherOverviewView.as_view(), name='weather-update-delete'),
]