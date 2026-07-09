import requests
import pandas as pd
from sqlalchemy import create_engine

# ==========================
# Supabase Connection
# ==========================
DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

engine = create_engine(DATABASE_URL)

# ==========================
# Karachi Coordinates
# ==========================
LATITUDE = 24.8607
LONGITUDE = 67.0011

# ==========================
# Open-Meteo API
# ==========================
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    f"&hourly=temperature_2m,relative_humidity_2m,rain,"
    f"wind_speed_10m,cloud_cover"
    f"&forecast_days=7"
    f"&timezone=Asia/Karachi"
)

print("Downloading weather data...")

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"API Error: {response.status_code}")

data = response.json()

print("Weather data downloaded.")

# ==========================
# Create DataFrame
# ==========================

weather = pd.DataFrame({
    "datetime": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "rain": data["hourly"]["rain"],
    "wind_speed": data["hourly"]["wind_speed_10m"],
    "cloud_cover": data["hourly"]["cloud_cover"]
})

weather["datetime"] = pd.to_datetime(weather["datetime"])

print(weather.head())

print(f"\nRows downloaded: {len(weather)}")

# ==========================
# Upload to Supabase
# ==========================

weather.to_sql(
    "weather",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("\nWeather uploaded successfully!")