import pandas as pd
from config import engine

print("=" * 60)
print("Merging Office Timings...")
print("=" * 60)

df = pd.read_csv(
    "ml/datasets/base_dataset.csv",
    parse_dates=["prediction_datetime"]
)

offices = pd.read_sql("SELECT * FROM office_timings", engine)

df["office_peak"] = 0

df["hour"] = df["prediction_datetime"].dt.hour

for _, row in offices.iterrows():

    open_hour = int(str(row["opening_time"]).split(":")[0])
    close_hour = int(str(row["closing_time"]).split(":")[0])

    mask = (
        (df["hour"] >= open_hour) &
        (df["hour"] <= close_hour)
    )

    df.loc[mask, "office_peak"] = 1

print(df["office_peak"].value_counts())

df.to_csv(
    "ml/datasets/base_dataset.csv",
    index=False
)

print("Office timings merged successfully.")