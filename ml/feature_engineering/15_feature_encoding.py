import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("=" * 60)
print("Encoding Features")
print("=" * 60)

df = pd.read_csv("ml/datasets/final_dataset.csv")

encoder = LabelEncoder()
level_encoder = LabelEncoder()

categorical = ["road_type"]
target = "traffic_level"

for col in categorical:
    df[col] = df[col].astype(str)
    df[col] = encoder.fit_transform(df[col])

df[target] = df[target].astype(str)
df[target] = level_encoder.fit_transform(df[target])

df.to_csv(
    "ml/datasets/final_dataset_encoded.csv",
    index=False
)

print(df.head())

print("Encoding Complete")