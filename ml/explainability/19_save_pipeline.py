import os
import json
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("=" * 60)
print("Saving ML Pipeline")
print("=" * 60)

os.makedirs("ml/models", exist_ok=True)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv("ml/datasets/final_dataset.csv")

# --------------------------------------------------
# Encode target
# --------------------------------------------------

encoder = LabelEncoder()

encoder.fit(df["traffic_level"])

joblib.dump(
    encoder,
    "ml/models/target_encoder.pkl"
)

print("Saved target_encoder.pkl")

# --------------------------------------------------
# Feature columns
# --------------------------------------------------

drop_columns = [
    "road_name",
    "geometry",
    "prediction_datetime",
    "traffic_score",
    "traffic_level"
]

feature_columns = [
    c for c in df.columns
    if c not in drop_columns
]

joblib.dump(
    feature_columns,
    "ml/models/feature_columns.pkl"
)

print("Saved feature_columns.pkl")

# --------------------------------------------------
# Metadata
# --------------------------------------------------

metadata = {

    "model_name": "Karachi Traffic Intelligence XGBoost",

    "version": "1.0",

    "problem_type": "Multi-class Classification",

    "target": "traffic_level",

    "classes": encoder.classes_.tolist(),

    "number_of_features": len(feature_columns),

    "feature_columns": feature_columns

}

with open(
    "ml/models/model_metadata.json",
    "w"
) as f:

    json.dump(
        metadata,
        f,
        indent=4
    )

print("Saved model_metadata.json")

print()

print("=" * 60)
print("Pipeline Saved Successfully")
print("=" * 60)