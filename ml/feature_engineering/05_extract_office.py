import pandas as pd
from config import engine

print("=" * 60)
print("Extracting Office Timings from Supabase...")
print("=" * 60)

query = """
SELECT
    sector,
    opening_time,
    closing_time
FROM office_timings
ORDER BY sector;
"""

offices = pd.read_sql(query, engine)

print("\nOffice timings loaded successfully.\n")

print("Dataset Shape:")
print(offices.shape)

print("\nFirst Five Rows:")
print(offices.head())

print("\nColumn Names:")
print(list(offices.columns))

print("\nData Types:")
print(offices.dtypes)

print("\nMissing Values:")
print(offices.isnull().sum())

# Remove duplicate rows
offices = offices.drop_duplicates()

# Convert to time format
offices["opening_time"] = pd.to_datetime(
    offices["opening_time"].astype(str)
).dt.time

offices["closing_time"] = pd.to_datetime(
    offices["closing_time"].astype(str)
).dt.time

print("\nNumber of Office Sectors:")
print(offices["sector"].nunique())

print("\nOffice Sectors:")
print(offices["sector"].unique())

print("\nSaving office timings dataset...")

offices.to_csv(
    "ml/datasets/office_timings_raw.csv",
    index=False
)

print("\nOffice timings dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/office_timings_raw.csv")