import pandas as pd
from config import engine

print("=" * 60)
print("Extracting Holiday Data from Supabase...")
print("=" * 60)

query = """
SELECT
    holiday_date,
    holiday_name,
    holiday_type,
    is_public
FROM holidays
ORDER BY holiday_date;
"""

holidays = pd.read_sql(query, engine)

print("\nHoliday data loaded successfully.\n")

print("Dataset Shape:")
print(holidays.shape)

print("\nFirst Five Rows:")
print(holidays.head())

print("\nColumn Names:")
print(list(holidays.columns))

print("\nData Types:")
print(holidays.dtypes)

print("\nMissing Values:")
print(holidays.isnull().sum())

# Convert holiday_date to datetime
holidays["holiday_date"] = pd.to_datetime(holidays["holiday_date"])

# Remove duplicate holidays
holidays = holidays.drop_duplicates(subset=["holiday_date"])

# Sort by date
holidays = holidays.sort_values("holiday_date")

print("\nHoliday Types:")
print(holidays["holiday_type"].value_counts())

print("\nPublic Holidays:")
print(holidays["is_public"].value_counts())

print("\nDate Range:")
print("Start :", holidays["holiday_date"].min())
print("End   :", holidays["holiday_date"].max())

print("\nSaving holiday dataset...")

holidays.to_csv(
    "ml/datasets/holidays_raw.csv",
    index=False
)

print("\nHoliday dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/holidays_raw.csv")