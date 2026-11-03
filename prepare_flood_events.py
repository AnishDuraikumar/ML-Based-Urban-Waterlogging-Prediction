
import pandas as pd

df = pd.read_csv("India_Flood_Inventory_v3.csv")

df["Start Date"] = pd.to_datetime(
    df["Start Date"],
    errors="coerce",
    format="mixed",
    dayfirst=True
)

# Select events recorded in 2023
df = df[df["Start Date"].dt.year == 2023].copy()

# Normalize cause descriptions for consistent filtering
df["Main Cause"] = df["Main Cause"].fillna("").str.lower().str.strip()

# Retain causes explicitly mentioning floods or inundation
flood_mask = df["Main Cause"].str.contains(
    r"\bfloods?\b|\binundation\b|\bwaterlogging\b",
    regex=True,
    na=False
)

floods = df.loc[flood_mask].copy()

# Remove records without district names
floods = floods.dropna(subset=["Districts"])

# Clean whitespace and remove duplicate records
floods["Districts"] = (
    floods["Districts"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

floods = floods.drop_duplicates(
    subset=["Start Date", "State", "Districts", "Main Cause"]
)

# Keep only the columns we need initially
floods = floods[
    ["Start Date", "End Date", "State", "Districts", "Main Cause"]
].copy()

floods.to_csv("flood_events_2023.csv", index=False)

print("===== FILTERED FLOOD EVENTS =====")
print("Records:", len(floods))
print("Unique dates:", floods["Start Date"].nunique())
print("States/regions:", floods["State"].nunique())
print("Missing district names:", floods["Districts"].isna().sum())

print("\n===== CAUSES =====")
print(floods["Main Cause"].value_counts().head(15).to_string())

print("\nSaved as flood_events_2023.csv")
