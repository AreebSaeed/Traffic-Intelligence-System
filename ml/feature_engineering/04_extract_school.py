import pandas as pd
from config import engine

print("=" * 60)
print("Extracting School Timings from Supabase...")
print("=" * 60)

query = """
SELECT
    school_type,
    opening_time,
    closing_time
FROM school_timings
ORDER BY school_type;
"""

schools = pd.read_sql(query, engine)

print("\nSchool timings loaded successfully.\n")

print("Dataset Shape:")
print(schools.shape)

print("\nFirst Five Rows:")
print(schools.head())

print("\nColumn Names:")
print(list(schools.columns))

print("\nData Types:")
print(schools.dtypes)

print("\nMissing Values:")
print(schools.isnull().sum())

# Remove duplicates
schools = schools.drop_duplicates()

# Convert to time format
schools["opening_time"] = pd.to_datetime(
    schools["opening_time"].astype(str)
).dt.time

schools["closing_time"] = pd.to_datetime(
    schools["closing_time"].astype(str)
).dt.time

print("\nNumber of School Types:")
print(schools["school_type"].nunique())

print("\nSchool Types:")
print(schools["school_type"].unique())

print("\nSaving school timings dataset...")

schools.to_csv(
    "ml/datasets/school_timings_raw.csv",
    index=False
)

print("\nSchool timings dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/school_timings_raw.csv")