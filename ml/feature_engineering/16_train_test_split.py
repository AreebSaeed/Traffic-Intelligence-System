import pandas as pd
from sklearn.model_selection import train_test_split

print("=" * 60)
print("Train / Test Split")
print("=" * 60)

df = pd.read_csv("ml/datasets/final_dataset_encoded.csv")

target = "traffic_level"

drop_columns = [
    "road_name",
    "geometry",
    "prediction_datetime",
    "holiday_name",
    "event_name",
    "event_type",
    "temperature_y",
    "humidity_y",
    "rain_y",
    "wind_speed_y",
    "cloud_cover_y",
    "traffic_score",
    target,
]

feature_columns = [col for col in df.columns if col not in drop_columns]

X = df[feature_columns].copy()

for col in ["lanes", "maxspeed"]:
    if col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")

X = X.fillna(0)

y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print(f"Features: {len(feature_columns)}")
print(f"Train rows: {len(X_train):,}")
print(f"Test rows: {len(X_test):,}")

X_train.to_csv("ml/datasets/X_train.csv", index=False)
X_test.to_csv("ml/datasets/X_test.csv", index=False)
y_train.to_csv("ml/datasets/y_train.csv", index=False)
y_test.to_csv("ml/datasets/y_test.csv", index=False)

print("Train/test split saved.")
