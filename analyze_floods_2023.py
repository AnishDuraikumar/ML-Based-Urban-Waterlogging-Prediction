
import pandas as pd

file_path = "India_Flood_Inventory_v3.csv"

df = pd.read_csv(file_path)

# Parse event start dates
df["Start Date"] = pd.to_datetime(
    df["Start Date"],
    errors="coerce",
    format="mixed",
    dayfirst=True
)

# Select records from 2023
df23 = df[df["Start Date"].dt.year == 2023].copy()

print("===== FLOOD INVENTORY: 2023 =====")
print("Total records:", len(df23))

print("\n===== MISSING VALUES =====")
print(
    df23[["Start Date", "State", "Districts", "Main Cause"]]
    .isnull()
    .sum()
)

print("\n===== UNIQUE STATES =====")
print("Number of states/regions:", df23["State"].nunique())
print(df23["State"].value_counts().head(15).to_string())

print("\n===== DISTRICT INFORMATION =====")
print("Records with district names:",
      df23["Districts"].notna().sum())
print("Records without district names:",
      df23["Districts"].isna().sum())

print("\n===== EXAMPLE FLOOD RECORDS =====")
print(
    df23[["Start Date", "State", "Districts", "Main Cause"]]
    .head(15)
    .to_string(index=False)
)
