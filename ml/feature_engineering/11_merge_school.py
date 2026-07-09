import pandas as pd

print("=" * 60)
print("Merging School Timings...")
print("=" * 60)

df = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

schools = pd.read_csv(
    "ml/datasets/school_timings_raw.csv"
)

# Initialize
df["school_peak"] = 0

# Convert hour
df["hour"] = df["prediction_datetime"].dt.hour

for _, row in schools.iterrows():

    open_hour = int(str(row["opening_time"]).split(":")[0])
    close_hour = int(str(row["closing_time"]).split(":")[0])

    mask = (
        (df["hour"] >= open_hour - 1) &
        (df["hour"] <= close_hour)
    )

    df.loc[mask, "school_peak"] = 1

print(df["school_peak"].value_counts())

df.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("School timings merged successfully.")