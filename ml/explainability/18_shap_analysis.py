import os
import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("SHAP Explainability")
print("=" * 60)

# -------------------------
# Load model
# -------------------------

model = joblib.load("ml/models/xgboost_model.pkl")

# -------------------------
# Load training data
# -------------------------

X_train = pd.read_csv("ml/datasets/X_train.csv")

SAMPLE_SIZE = 5000
if len(X_train) > SAMPLE_SIZE:
    X_train = X_train.sample(n=SAMPLE_SIZE, random_state=42)
    print(f"Using {SAMPLE_SIZE:,} sampled rows for SHAP (faster analysis)")

print(f"Training Samples: {len(X_train)}")
print(f"Features: {X_train.shape[1]}")

# -------------------------
# Create Explainer
# -------------------------

explainer = shap.TreeExplainer(model)

print("Calculating SHAP values...")

shap_values = explainer.shap_values(X_train)

print("Done!")

# -------------------------
# Create output folder
# -------------------------

os.makedirs("ml/results", exist_ok=True)

# -------------------------
# Global Feature Importance
# -------------------------

plt.figure(figsize=(12, 8))

shap.summary_plot(
    shap_values,
    X_train,
    show=False
)

plt.tight_layout()

plt.savefig(
    "ml/results/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved: ml/results/shap_summary.png")

# -------------------------
# Bar Plot
# -------------------------

plt.figure(figsize=(10, 8))

shap.summary_plot(
    shap_values,
    X_train,
    plot_type="bar",
    show=False
)

plt.tight_layout()

plt.savefig(
    "ml/results/shap_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved: ml/results/shap_bar.png")
