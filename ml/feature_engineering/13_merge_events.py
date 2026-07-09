import pandas as pd

print("=" * 60)
print("Merging Events...")
print("=" * 60)

df = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

events = pd.read_csv(
    "ml/datasets/events_raw.csv",
    parse_dates=["event_date"]
)

# Extract date
df["date"] = df["prediction_datetime"].dt.date
events["date"] = events["event_date"].dt.date

df = df.merge(
    events[["date", "event_name", "event_type"]],
    on="date",
    how="left"
)

df["event"] = df["event_name"].notna().astype(int)

df.drop(columns=["date"], inplace=True)

print(df["event"].value_counts())

df.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("Events merged successfully.")