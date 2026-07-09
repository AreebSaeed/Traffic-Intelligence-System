import pandas as pd
from config import engine

print("=" * 60)
print("Merging Weather Data...")
print("=" * 60)

base = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

weather = pd.read_sql("SELECT * FROM weather", engine)
weather["datetime"] = pd.to_datetime(weather["datetime"])

print("Base:", base.shape)
print("Weather:", weather.shape)

weather = weather.rename(columns={
    "temperature": "temperature",
    "humidity": "humidity",
    "rain": "rain",
    "wind_speed": "wind_speed"
})

base = base.merge(
    weather,
    left_on="prediction_datetime",
    right_on="datetime",
    how="left"
)

base.drop(columns=["datetime"], inplace=True)

print(base.head())

base.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("Weather merged successfully.")