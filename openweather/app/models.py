from django.db import models

class Weather(models.Model):
    location_name = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    weather_overview = models.TextField(blank=True)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location_name} ({self.lat}, {self.lon}) - {self.weather_overview}"