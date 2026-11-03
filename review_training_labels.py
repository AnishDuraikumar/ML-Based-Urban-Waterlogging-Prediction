
import pandas as pd

df = pd.read_csv(
    "district_rainfall_features_2023.csv",
    parse_dates=["Date"]
)

print("===== LABEL REVIEW =====")
print("Total district-day rows:", len(df))
print("Recorded-event rows:", int(df["Recorded_Flood_Event"].sum()))
print(
    "Rows without a matched event:",
    int((df["Recorded_Flood_Event"] == 0).sum())
)

print("\n===== RECORDED EVENT ROWS BY MONTH =====")
events = df[df["Recorded_Flood_Event"] == 1].copy()
print(events.groupby(events["Date"].dt.month).size().to_string())

print("\n===== FEATURE MISSING VALUES =====")
features = [
    "Mean_Rainfall_mm",
    "Max_Rainfall_mm",
    "Rainfall_Previous_3_Days_mm",
    "Rainfall_Previous_7_Days_mm",
    "Rainfall_3_Day_Total_mm",
    "Rainfall_7_Day_Total_mm"
]
print(df[features].isna().sum().to_string())

print("\n===== EXAMPLE EVENT ROWS =====")
print(
    events[
        ["Date", "State", "District", "Mean_Rainfall_mm",
         "Rainfall_Previous_3_Days_mm",
         "Rainfall_Previous_7_Days_mm"]
    ].head(10).to_string(index=False)
)

print("\nReview complete. No model has been trained yet.")
            