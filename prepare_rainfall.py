
import xarray as xr
import pandas as pd

file_path = "RF25_ind2023_rfp25.nc"

with xr.open_dataset(file_path) as ds:
    rainfall = ds["RAINFALL"]

    # Keep grid locations with at least 300 valid days
    valid_days = rainfall.count(dim="TIME")
    usable_mask = valid_days >= 300

    # Extract only usable locations
    clean_rainfall = rainfall.where(usable_mask)

    # Convert to a table and remove missing rainfall readings
    df = clean_rainfall.to_dataframe(
        name="Rainfall_mm"
    ).reset_index()

    df = df.dropna(subset=["Rainfall_mm"]).copy()

    # Use consistent column names
    df = df.rename(columns={
        "TIME": "Date",
        "LATITUDE": "Latitude",
        "LONGITUDE": "Longitude"
    })

    df["Date"] = pd.to_datetime(df["Date"])

    # Save cleaned data
    df.to_csv("rainfall_2023_clean.csv", index=False)

    print("===== CLEAN RAINFALL DATA =====")
    print("Rows:", len(df))
    print("Unique dates:", df["Date"].nunique())
    print("Unique grid locations:",
          df[["Latitude", "Longitude"]].drop_duplicates().shape[0])
    print("Missing rainfall values:", df["Rainfall_mm"].isna().sum())
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    print("\nSaved as rainfall_2023_clean.csv")


