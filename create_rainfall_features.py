
import pandas as pd

df = pd.read_csv(
    "district_rainfall_event_analysis.csv",
    parse_dates=["Date"]
)

df = df.sort_values(["State", "District", "Date"]).copy()

groups = df.groupby(["State", "District"], sort=False)

# Rainfall accumulated over the previous days,
# excluding the current day.
df["Rainfall_Previous_3_Days_mm"] = groups[
    "Mean_Rainfall_mm"
].transform(
    lambda s: s.shift(1).rolling(3, min_periods=3).sum()
)

df["Rainfall_Previous_7_Days_mm"] = groups[
    "Mean_Rainfall_mm"
].transform(
    lambda s: s.shift(1).rolling(7, min_periods=7).sum()
)

# Current day + previous 2 days
df["Rainfall_3_Day_Total_mm"] = groups[
    "Mean_Rainfall_mm"
].transform(
    lambda s: s.rolling(3, min_periods=3).sum()
)

# Current day + previous 6 days
df["Rainfall_7_Day_Total_mm"] = groups[
    "Mean_Rainfall_mm"
].transform(
    lambda s: s.rolling(7, min_periods=7).sum()
)

df.to_csv("district_rainfall_features_2023.csv", index=False)

print("===== RAINFALL FEATURES CREATED =====")
print("Rows:", len(df))
print("Districts:", df["District"].nunique())

feature_cols = [
    "Mean_Rainfall_mm",
    "Max_Rainfall_mm",
    "Rainfall_Previous_3_Days_mm",
    "Rainfall_Previous_7_Days_mm",
    "Rainfall_3_Day_Total_mm",
    "Rainfall_7_Day_Total_mm"
]

print("\n===== FEATURE SUMMARY =====")
print(df[feature_cols].describe().round(2).to_string())

events = df[df["Recorded_Flood_Event"] == 1]

print("\n===== MATCHED EVENT-DAY RAINFALL =====")
print(
    events[feature_cols].describe().round(2).to_string()
)

print("\nSaved as district_rainfall_features_2023.csv")
