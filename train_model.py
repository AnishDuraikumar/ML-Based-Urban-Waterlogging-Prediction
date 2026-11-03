
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Load dataset
df = pd.read_csv("district_rainfall_features_2023.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 2. Select features and target
features = [
    "Mean_Rainfall_mm",
    "Max_Rainfall_mm",
    "Rainfall_Previous_3_Days_mm",
    "Rainfall_Previous_7_Days_mm",
    "Rainfall_3_Day_Total_mm",
    "Rainfall_7_Day_Total_mm"
]
target = "Recorded_Flood_Event"

# 3. Remove rows with missing rainfall features
df = df.dropna(subset=features).copy()
df = df.sort_values("Date")

# 4. Chronological training/testing split
split_date = pd.Timestamp("2023-08-01")

train = df[df["Date"] < split_date]
test = df[df["Date"] >= split_date]

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

print("===== DATA SPLIT =====")
print("Training rows:", len(train))
print("Testing rows:", len(test))
print("Training recorded events:", int(y_train.sum()))
print("Testing recorded events:", int(y_test.sum()))

if y_train.nunique() < 2 or y_test.nunique() < 2:
    print("ERROR: Training or testing data has only one class.")

else:
    # 5. Train Random Forest
    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    joblib.dump(model, "flood_risk_model.pkl")
    print("Trained model saved as flood_risk_model.pkl")

    # 6. Calculate event probabilities
    probabilities = model.predict_proba(X_test)[:, 1]

    print("\n===== RAINFALL FEATURE COMPARISON =====")
    comparison = test.groupby(target)[features].mean().round(2)
    print(comparison.to_string())

    print("\n===== PREDICTION PROBABILITIES =====")
    print("Minimum:", probabilities.min())
    print("Maximum:", probabilities.max())
    print("Mean:", round(probabilities.mean(), 6))

    print("\n===== MODEL EVALUATION AT THRESHOLD 0.01 =====")
    threshold = 0.01
    predictions = (probabilities >= threshold).astype(int)

    print("Threshold:", threshold)
    print("Alerts generated:", int(predictions.sum()))
    print("Actual recorded events:", int(y_test.sum()))
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("Precision:", round(
        precision_score(y_test, predictions, zero_division=0), 4
    ))
    print("Recall:", round(
        recall_score(y_test, predictions, zero_division=0), 4
    ))
    print("F1 score:", round(
        f1_score(y_test, predictions, zero_division=0), 4
    ))

    print("\n===== CONFUSION MATRIX =====")
    print(confusion_matrix(y_test, predictions))

    print("\n===== CLASSIFICATION REPORT =====")
    print(classification_report(
        y_test, predictions, zero_division=0
    ))

    # 7. Compare thresholds
    print("\n===== THRESHOLD COMPARISON =====")

    for threshold in [0.005, 0.01, 0.02, 0.05, 0.10]:
        threshold_predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_test, threshold_predictions, zero_division=0
        )
        recall = recall_score(
            y_test, threshold_predictions, zero_division=0
        )
        f1 = f1_score(
            y_test, threshold_predictions, zero_division=0
        )

        print(
            f"Threshold: {threshold:.3f} | "
            f"Alerts: {int(threshold_predictions.sum())} | "
            f"Precision: {precision:.4f} | "
            f"Recall: {recall:.4f} | "
            f"F1: {f1:.4f}"
        )

    print("\n===== PROJECT LIMITATIONS =====")
    print("Unmatched days are not confirmed flood-free days.")
    print("Results use 2023 data and require further validation.")

