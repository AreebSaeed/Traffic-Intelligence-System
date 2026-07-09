import pandas as pd
import numpy as np

print("=" * 60)
print("Generating Traffic Labels")
print("=" * 60)

df = pd.read_csv("ml/datasets/base_dataset.csv")

rain = df["rain_x"] if "rain_x" in df.columns else df["rain"]
cloud_cover = df["cloud_cover_x"] if "cloud_cover_x" in df.columns else df["cloud_cover"]

score = np.zeros(len(df))

# Rain
score += np.where(rain > 0, 30, 0)

# Office peak
score += df["office_peak"] * 25

# School peak
score += df["school_peak"] * 20

# Holiday
score -= df["is_holiday"] * 15

# Events
score += df["event"] * 20

# Cloud cover
score += np.where(cloud_cover > 70, 5, 0)

# Random variation
score += np.random.randint(0, 20, len(df))

df["traffic_score"] = score

df["traffic_level"] = pd.cut(
    score,
    bins=[-1, 30, 60, 100],
    labels=["Low", "Medium", "High"]
)

print(df["traffic_level"].value_counts())

df.to_csv(
    "ml/datasets/final_dataset.csv",
    index=False
)

print("Traffic labels generated.")