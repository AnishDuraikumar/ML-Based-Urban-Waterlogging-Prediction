
import pandas as pd

df = pd.read_csv("district_rainfall_event_analysis.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("===== DATASET OVERVIEW =====")
print("Total rows:", len(df))
print("Unique districts:", df["District"].nunique())
print("Unique dates:", df["Date"].nunique())

print("\n===== EVENT LABEL COUNTS =====")
print(df["Recorded_Flood_Event"].value_counts().to_string())

events = df[df["Recorded_Flood_Event"] == 1].copy()

print("\n===== RAINFALL ON MATCHED EVENT DAYS =====")
if len(events) > 0:
    print(
        events[
            ["Mean_Rainfall_mm", "Max_Rainfall_mm", "Grid_Cells"]
        ].describe().round(2).to_string()
    )

    print("\n===== SAMPLE MATCHED EVENTS =====")
    print(
        events[
            [
                "Date", "State", "District",
                "Mean_Rainfall_mm", "Max_Rainfall_mm"
            ]
        ].head(15).to_string(index=False)
    )
else:
    print("No matched events were found.")

print("\n===== RAINFALL DATA CHECK =====")
print("Missing mean rainfall:",
      df["Mean_Rainfall_mm"].isna().sum())
print("Negative mean rainfall:",
      (df["Mean_Rainfall_mm"] < 0).sum())

print("\nAnalysis complete.")
