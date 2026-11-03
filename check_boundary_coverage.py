
import json
import pandas as pd
import re
import unicodedata

def normalize(value):
    if pd.isna(value):
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

# Read boundary data
with open("india_district.geojson", encoding="utf-8") as f:
    geo = json.load(f)

features = geo["features"]
boundary_pairs = set()

for feature in features:
    props = feature.get("properties", {})
    boundary_pairs.add((
        normalize(props.get("NAME_1")),
        normalize(props.get("NAME_2"))
    ))

# Read flood records
floods = pd.read_csv("flood_events_2023.csv")
floods["Districts"] = floods["Districts"].fillna("").astype(str)
floods["Districts"] = floods["Districts"].str.split(",")
floods = floods.explode("Districts")
floods["Districts"] = floods["Districts"].str.strip()

floods["state_key"] = floods["State"].apply(normalize)
floods["district_key"] = floods["Districts"].apply(normalize)

floods["Boundary_Match"] = [
    (state, district) in boundary_pairs
    for state, district in zip(
        floods["state_key"], floods["district_key"]
    )
]

print("===== BOUNDARY COVERAGE =====")
print("Exploded flood-district records:", len(floods))
print("Matched records:", int(floods["Boundary_Match"].sum()))
print("Unmatched records:", int((~floods["Boundary_Match"]).sum()))

print("\n===== MATCHING BY STATE =====")
print(
    floods.groupby("State")["Boundary_Match"]
    .agg(["count", "sum"])
    .sort_values("sum")
    .to_string()
)

floods.to_csv("flood_boundary_coverage.csv", index=False)
print("\nSaved as flood_boundary_coverage.csv")
