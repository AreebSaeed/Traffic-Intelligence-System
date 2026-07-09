import pandas as pd
from config import engine

print("=" * 60)
print("Extracting Events from Supabase...")
print("=" * 60)

query = """
SELECT
    event_name,
    event_date,
    location,
    event_type
FROM events
ORDER BY event_date;
"""

events = pd.read_sql(query, engine)

print("\nEvents loaded successfully.\n")

print("Dataset Shape:")
print(events.shape)

print("\nFirst Five Rows:")
print(events.head())

print("\nColumn Names:")
print(list(events.columns))

print("\nData Types:")
print(events.dtypes)

print("\nMissing Values:")
print(events.isnull().sum())

# Convert event_date to datetime
events["event_date"] = pd.to_datetime(events["event_date"])

# Remove duplicate events
events = events.drop_duplicates()

# Sort by date
events = events.sort_values("event_date")

print("\nNumber of Event Types:")
print(events["event_type"].nunique())

print("\nEvent Types:")
print(events["event_type"].value_counts())

print("\nDate Range:")
print("Start :", events["event_date"].min())
print("End   :", events["event_date"].max())

print("\nSaving events dataset...")

events.to_csv(
    "ml/datasets/events_raw.csv",
    index=False
)

print("\nEvents dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/events_raw.csv")