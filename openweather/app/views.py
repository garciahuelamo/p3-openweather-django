import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Weather

class WeatherOverviewView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": "Latitude and Longitude are required"}, status=400)
        
        api_key = settings.OPENWEATHER_API_KEY

        if not api_key:
            return Response({"error": "API Key is missing"}, status=500)
        
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(weather_url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch weather data"}, status=response.status_code)
        
        data = response.json()
        weather_overview = data.get("weather", [{}])[0].get("description", "No data available")
        location_name = data.get("name", "Unknown Location")
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        weather_entry = Weather.objects.create(
            location_name=location_name,
            lat=lat,
            lon=lon,
            weather_overview=weather_overview,
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
        )

        return Response({
            "id": weather_entry.id,  # Devuelve el ID del registro guardado
            "location_name": location_name,
            "lat": lat,
            "lon": lon,
            "weather_overview": weather_overview,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
        })
    
    def post(self, request, *args, **kwargs):
        data = request.data

        if not data.get("lat") or not data.get("lon"):
            return Response({"error": "Latitude and Longitude are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        weather_entry = Weather.objects.create(
            location_name=data.get("location_name", "Unknown Location"),
            lat=data["lat"],
            lon=data["lon"],
            weather_overview=data.get("weather_overview", "No description"),
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"],
        )

        return Response({
            "id": weather_entry.id,
            "location_name": weather_entry.location_name,
            "lat": weather_entry.lat,
            "lon": weather_entry.lon,
            "weather_overview": weather_entry.weather_overview,
            "temperature": weather_entry.temperature,
            "humidity": weather_entry.humidity,
            "pressure": weather_entry.pressure,
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        weather_id = kwargs.get("weather_id")
        data = request.data

        try:
            weather_entry = Weather.objects.get(id=weather_id)
        except Weather.DoesNotExist:
            return Response({"error": "Weather entry not found"}, status=status.HTTP_404_NOT_FOUND)
        
        weather_entry.location_name = data.get("location_name", weather_entry.location_name)
        weather_entry.lat = data.get("lat", weather_entry.lat)
        weather_entry.lon = data.get("lon", weather_entry.lon)
        weather_entry.weather_overview = data.get("weather_overview", weather_entry.weather_overview)
        weather_entry.temperature = data.get("temperature", weather_entry.temperature)
        weather_entry.humidity = data.get("humidity", weather_entry.humidity)
        weather_entry.pressure = data.get("pressure", weather_entry.pressure)

        weather_entry.save()

        return Response({
            "id": weather_entry.id,
            "location_name": weather_entry.location_name,
            "lat": weather_entry.lat,
            "lon": weather_entry.lon,
            "weather_overview": weather_entry.weather_overview,
            "temperature": weather_entry.temperature,
            "humidity": weather_entry.humidity,
            "pressure": weather_entry.pressure,
        })