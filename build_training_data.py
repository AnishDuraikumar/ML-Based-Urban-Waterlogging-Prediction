
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

# Load daily rainfall summaries
rain = pd.read_csv(
    "district_daily_rainfall_2023.csv",
    parse_dates=["Date"]
)

rain["State_Key"] = rain["State"].apply(normalize)
rain["District_Key"] = rain["District"].apply(normalize)

# Load recorded flood events
floods = pd.read_csv("flood_events_2023.csv")
floods["Start Date"] = pd.to_datetime(
    floods["Start Date"], errors="coerce", format="mixed"
)

# Split rows containing multiple districts
floods["Districts"] = floods["Districts"].fillna("").astype(str)
floods["Districts"] = floods["Districts"].str.split(",")
floods = floods.explode("Districts")
floods["Districts"] = floods["Districts"].str.strip()

floods["State_Key"] = floods["State"].apply(normalize)
floods["District_Key"] = floods["Districts"].apply(normalize)

# Mark recorded flood-related district-days
floods["Date"] = floods["Start Date"].dt.normalize()

event_keys = floods[
    ["Date", "State_Key", "District_Key"]
].drop_duplicates()

event_keys["Recorded_Flood_Event"] = 1

# Join events to rainfall by date, state and district
data = rain.merge(
    event_keys,
    on=["Date", "State_Key", "District_Key"],
    how="left"
)

data["Recorded_Flood_Event"] = (
    data["Recorded_Flood_Event"].fillna(0).astype(int)
)

print("===== EVENT JOIN CHECK =====")
print("Rainfall rows:", len(rain))
print("Rows with recorded flood event:",
      int(data["Recorded_Flood_Event"].sum()))
print("Distinct event dates matched:",
      data.loc[data["Recorded_Flood_Event"] == 1, "Date"].nunique())
print("Unmatched flood district-days:",
      len(event_keys.merge(
          rain[["Date", "State_Key", "District_Key"]].drop_duplicates(),
          on=["Date", "State_Key", "District_Key"],
          how="left",
          indicator=True
      ).query("_merge == 'left_only'")))

# Save as an event-analysis table, not yet a training dataset
data.to_csv("district_rainfall_event_analysis.csv", index=False)
print("\nSaved as district_rainfall_event_analysis.csv")
print("Note: zero labels are not confirmed flood-free days.")
