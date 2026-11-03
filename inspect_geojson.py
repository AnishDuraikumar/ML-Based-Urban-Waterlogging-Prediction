
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

# Read geographic boundaries
with open("india_district.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

boundary_rows = []

for feature in geo["features"]:
    props = feature.get("properties", {})
    boundary_rows.append({
        "State": props.get("NAME_1"),
        "District": props.get("NAME_2")
    })

boundaries = pd.DataFrame(boundary_rows)
boundaries["state_key"] = boundaries["State"].apply(normalize_name)
boundaries["district_key"] = boundaries["District"].apply(normalize_name)

# Read flood records
floods = pd.read_csv("flood_events_2023.csv")
floods["Districts"] = floods["Districts"].fillna("").astype(str)

# Split multiple district names into separate rows
floods["Districts"] = floods["Districts"].str.split(",")
floods = floods.explode("Districts")
floods["Districts"] = floods["Districts"].str.strip()

floods["state_key"] = floods["State"].apply(normalize_name)
floods["district_key"] = floods["Districts"].apply(normalize_name)

# Compare using both state and district
boundary_pairs = set(zip(
    boundaries["state_key"],
    boundaries["district_key"]
))

flood_pairs = set(zip(
    floods["state_key"],
    floods["district_key"]
))

matched = flood_pairs & boundary_pairs
unmatched = flood_pairs - boundary_pairs

print("===== STATE + DISTRICT MATCHING =====")
print("Unique state-district pairs:", len(flood_pairs))
print("Matching pairs:", len(matched))
print("Unmatched pairs:", len(unmatched))

print("\n===== UNMATCHED STATE-DISTRICT PAIRS =====")
for state, district in sorted(unmatched)[:60]:
    print(f"{state} | {district}")
