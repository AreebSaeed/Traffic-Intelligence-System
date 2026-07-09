import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

print("=" * 60)
print("Training XGBoost")
print("=" * 60)

X_train = pd.read_csv("ml/datasets/X_train.csv")
X_test = pd.read_csv("ml/datasets/X_test.csv")

y_train = pd.read_csv("ml/datasets/y_train.csv").squeeze()
y_test = pd.read_csv("ml/datasets/y_test.csv").squeeze()

model = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    random_state=42,
    eval_metric="mlogloss",
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print()
print("Accuracy")
print(accuracy_score(y_test, pred))

print()
print(classification_report(y_test, pred))

print()
print(confusion_matrix(y_test, pred))

joblib.dump(model, "ml/models/xgboost_model.pkl")

print()
print("Model Saved!")
