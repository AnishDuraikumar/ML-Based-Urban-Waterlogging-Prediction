
import pandas as pd

# Load the cleaned rainfall dataset
rainfall = pd.read_csv(
    "rainfall_2023_clean.csv",
    parse_dates=["Date"]
)

# Load the filtered flood inventory
floods = pd.read_csv(
    "flood_events_2023.csv",
    parse_dates=["Start Date"]
)

# Compare the dates available in each dataset
rainfall_dates = set(rainfall["Date"].dt.normalize().unique())
flood_dates = set(floods["Start Date"].dt.normalize().unique())

matching_dates = sorted(rainfall_dates & flood_dates)
flood_only_dates = sorted(flood_dates - rainfall_dates)

print("===== DATE MATCHING RESULTS =====")
print("Unique rainfall dates:", len(rainfall_dates))
print("Unique flood dates:", len(flood_dates))
print("Matching dates:", len(matching_dates))
print("Flood dates without rainfall data:", len(flood_only_dates))

print("\n===== FIRST 15 MATCHING DATES =====")
for date in matching_dates[:15]:
    print(pd.Timestamp(date).date())

print("\n===== FLOOD DATES WITHOUT RAINFALL =====")
for date in flood_only_dates[:10]:
    print(pd.Timestamp(date).date())
