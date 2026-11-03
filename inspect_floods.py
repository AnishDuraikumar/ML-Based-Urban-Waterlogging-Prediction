
import pandas as pd

df = pd.read_csv("India_Flood_Inventory_v3.csv")

df["Start Date"] = pd.to_datetime(
    df["Start Date"],
    errors="coerce",
    format="mixed",
    dayfirst=True
)

# Select records starting in 2023
df23 = df[df["Start Date"].dt.year == 2023].copy()

print("===== RECORDS BY MAIN CAUSE =====")
print(df23["Main Cause"].fillna("Missing").value_counts().to_string())

print("\n===== RECORDS BY YEAR =====")
print(df["Start Date"].dt.year.value_counts().sort_index().tail(15).to_string())

print("\n===== 2023 FLOOD-RELATED RECORDS =====")
mask = df23["Main Cause"].str.contains(
    "flood|inundation|waterlogging",
    case=False,
    na=False
)

print("Matching records:", int(mask.sum()))
print(df23.loc[mask, [
    "Start Date", "End Date", "State", "Districts", "Main Cause"
]].head(10).to_string(index=False))



