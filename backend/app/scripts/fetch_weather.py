"""Fetch weather data from OpenWeatherMap API."""
import httpx
from datetime import datetime
from geoalchemy2.elements import WKTElement

from app.database import SessionLocal
from app.models import WeatherReading
from app.config import settings


def fetch_weather():
    """
    Fetch current weather data from OpenWeatherMap for key locations
    along the Guwahati-Shillong corridor.

    Requires OPENWEATHERMAP_API_KEY in .env file.
    """
    if not settings.openweathermap_api_key:
        print("✗ OpenWeatherMap API key not configured")
        print("\nPlease add OPENWEATHERMAP_API_KEY to your .env file")
        print("Get a free key at: https://openweathermap.org/api")
        return

    print("Fetching weather data from OpenWeatherMap...\n")

    # Key locations along corridor
    locations = [
        {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362},
        {"name": "Nongpoh", "lat": 25.9015, "lon": 91.8797},
        {"name": "Shillong", "lat": 25.5788, "lon": 91.8933},
    ]

    db = SessionLocal()

    try:
        for location in locations:
            print(f"Fetching weather for {location['name']}...")

            try:
                # Call OpenWeatherMap API
                response = httpx.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "lat": location["lat"],
                        "lon": location["lon"],
                        "appid": settings.openweathermap_api_key,
                        "units": "metric"
                    },
                    timeout=10.0
                )

                if response.status_code != 200:
                    print(f"  ✗ API error: {response.status_code}")
                    continue

                data = response.json()

                # Extract weather parameters
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"] * 3.6  # m/s to km/h
                visibility = data.get("visibility", 10000) / 1000  # meters to km
                condition = data["weather"][0]["main"].lower()
                rain = data.get("rain", {}).get("1h", 0)  # mm in last hour

                # Create weather reading
                location_point = WKTElement(
                    f"POINT({location['lon']} {location['lat']})",
                    srid=4326
                )

                reading = WeatherReading(
                    latitude=location["lat"],
                    longitude=location["lon"],
                    location=location_point,
                    timestamp=datetime.utcnow(),
                    temperature_c=temp,
                    precipitation_mm=rain,
                    wind_speed_kmh=wind_speed,
                    humidity_percent=humidity,
                    visibility_km=visibility,
                    condition=condition,
                    source="openweathermap",
                    is_synthetic=False
                )

                db.add(reading)
                db.commit()

                print(f"  [OK] {temp:.1f}°C, {condition}, "
                      f"{rain:.1f}mm rain, {humidity}% humidity")

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")

        print("\n[OK] Weather data fetch complete!")
        print("\nNext step: Run python -m app.ml.score_segments to update risk scores")

    finally:
        db.close()


if __name__ == "__main__":
    fetch_weather()
