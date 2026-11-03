
import json
import re
import pandas as pd
import unicodedata

def normalize_name(value):
    if pd.isna(value):
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

with open("india_district.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

boundary_rows = [
    {
        "State": feature.get("properties", {}).get("NAME_1"),
        "District": feature.get("properties", {}).get("NAME_2")
    }
    for feature in geo["features"]
]

boundaries = pd.DataFrame(boundary_rows)
boundaries["state_key"] = boundaries["State"].apply(normalize_name)
boundaries["district_key"] = boundaries["District"].apply(normalize_name)

floods = pd.read_csv("flood_events_2023.csv")
floods["Districts"] = floods["Districts"].fillna("").astype(str)
floods["Districts"] = floods["Districts"].str.split(",")
floods = floods.explode("Districts")
floods["Districts"] = floods["Districts"].str.strip()

floods["state_key"] = floods["State"].apply(normalize_name)
floods["district_key"] = floods["Districts"].apply(normalize_name)

boundary_pairs = set(zip(boundaries["state_key"], boundaries["district_key"]))
boundary_lookup = boundaries.drop_duplicates(
    ["state_key", "district_key"]
).set_index(["state_key", "district_key"])

flood_pairs = set(zip(floods["state_key"], floods["district_key"]))
unmatched_pairs = sorted(flood_pairs - boundary_pairs)

rows = []
for state, district in unmatched_pairs:
    rows.append({
        "State_Normalized": state,
        "District_Normalized": district,
        "Verified_Boundary_District": "",
        "Review_Status": "Needs review"
    })

pd.DataFrame(rows).to_csv("unmatched_districts_review.csv", index=False)

print("Created unmatched_districts_review.csv")
print("Rows needing review:", len(rows))
print("Do not fill in district names until they are verified.")
