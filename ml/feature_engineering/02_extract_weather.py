import pandas as pd
from config import engine

print("=" * 60)
print("Extracting Weather Data from Supabase...")
print("=" * 60)

query = """
SELECT
    datetime,
    temperature,
    humidity,
    rain,
    wind_speed,
    cloud_cover
FROM weather
ORDER BY datetime;
"""

weather = pd.read_sql(query, engine)

print("\nWeather data loaded successfully.\n")

print("Dataset Shape:")
print(weather.shape)

print("\nFirst Five Rows:")
print(weather.head())

print("\nColumn Names:")
print(list(weather.columns))

print("\nData Types:")
print(weather.dtypes)

print("\nMissing Values:")
print(weather.isnull().sum())

print("\nSummary Statistics:")
print(weather.describe())

# Convert datetime column
weather["datetime"] = pd.to_datetime(weather["datetime"])

# Remove duplicate timestamps
weather = weather.drop_duplicates(subset=["datetime"])

# Sort chronologically
weather = weather.sort_values("datetime")

print("\nDate Range:")
print("Start :", weather["datetime"].min())
print("End   :", weather["datetime"].max())

print("\nAverage Temperature:")
print(round(weather["temperature"].mean(), 2), "°C")

print("\nMaximum Rainfall:")
print(round(weather["rain"].max(), 2), "mm")

print("\nMaximum Wind Speed:")
print(round(weather["wind_speed"].max(), 2), "km/h")

print("\nSaving weather dataset...")

weather.to_csv(
    "ml/datasets/weather_raw.csv",
    index=False
)

print("\nWeather dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/weather_raw.csv")