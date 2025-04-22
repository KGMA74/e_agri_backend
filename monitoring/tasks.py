from celery import shared_task
from farms.models import Farm
from .services import fetch_weather_for_location

@shared_task
def fetch_weather_all_farms():
    zones_seen = set()
    for farm in Farm.objets.all():
        key = (round(farm.latitude, 1), round(farm.longitude, 1))
        if key in zones_seen:
            continue
        fetch_weather_for_location(farm.latitude, farm.longitude, farm.zone)
        zones_seen.add(key)