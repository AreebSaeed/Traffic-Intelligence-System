import pandas as pd

print("=" * 60)
print("Merging Holiday Data...")
print("=" * 60)

base = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

holidays = pd.read_csv(
    "ml/datasets/holidays_raw.csv",
    parse_dates=["holiday_date"]
)

# Extract date only
base["date"] = base["prediction_datetime"].dt.date
holidays["date"] = holidays["holiday_date"].dt.date

base = base.merge(
    holidays[["date", "holiday_name"]],
    on="date",
    how="left"
)

base["is_holiday"] = base["holiday_name"].notna().astype(int)

base.drop(columns=["date"], inplace=True)

print(base.head())

base.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("Holiday data merged successfully.")