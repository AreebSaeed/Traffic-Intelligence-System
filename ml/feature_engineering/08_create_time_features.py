import pandas as pd

print("=" * 60)
print("Creating Time Features...")
print("=" * 60)

df = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

print(f"Loaded {len(df):,} rows")

# Create time features
df["hour"] = df["prediction_datetime"].dt.hour
df["day"] = df["prediction_datetime"].dt.day
df["month"] = df["prediction_datetime"].dt.month
df["weekday"] = df["prediction_datetime"].dt.dayofweek

df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)

# Peak hours
df["morning_peak"] = df["hour"].between(7, 9).astype(int)
df["evening_peak"] = df["hour"].between(16, 19).astype(int)

print(df.head())

df.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("Time features added successfully.")