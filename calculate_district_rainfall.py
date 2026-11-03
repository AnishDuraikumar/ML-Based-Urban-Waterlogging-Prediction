
import geopandas as gpd
import pandas as pd
import xarray as xr

print("Loading district boundaries...")
districts = gpd.read_file("india_district.geojson")

districts = districts[["NAME_1", "NAME_2", "geometry"]].copy()
districts = districts.rename(columns={
    "NAME_1": "State",
    "NAME_2": "District"
})

# Standardize names for matching
districts["State_Key"] = (
    districts["State"].str.lower().str.strip()
)
districts["District_Key"] = (
    districts["District"].str.lower().str.strip()
)

print("Loading rainfall grid...")
with xr.open_dataset("RF25_ind2023_rfp25.nc") as ds:
    rain = ds["RAINFALL"]

    # Convert grid-cell centers into points
    grid = pd.DataFrame([
        {"Latitude": lat, "Longitude": lon}
        for lat in rain["LATITUDE"].values
        for lon in rain["LONGITUDE"].values
    ])

    grid_gdf = gpd.GeoDataFrame(
        grid,
        geometry=gpd.points_from_xy(
            grid["Longitude"], grid["Latitude"]
        ),
        crs="EPSG:4326"
    )

    # Keep locations with enough valid rainfall data
    valid_days = rain.count(dim="TIME").to_dataframe(
        name="Valid_Days"
    ).reset_index()

    valid_days = valid_days[
        valid_days["Valid_Days"] >= 300
    ]

    grid_gdf = grid_gdf.merge(
        valid_days[["LATITUDE", "LONGITUDE"]],
        left_on=["Latitude", "Longitude"],
        right_on=["LATITUDE", "LONGITUDE"],
        how="inner"
    )

    print("Usable rainfall grid points:", len(grid_gdf))

    # Use a spatial join to assign grid points to districts
    matched = gpd.sjoin(
        grid_gdf,
        districts,
        how="inner",
        predicate="within"
    )

    print("Grid points matched to districts:", len(matched))
    print("Districts with grid points:", matched["District"].nunique())

    # Keep one record per grid point and district
    matched = matched.drop_duplicates(
        subset=["Latitude", "Longitude", "State", "District"]
    )

    # Extract daily rainfall values at usable grid points
    records = []

    for _, point in matched.iterrows():
        series = rain.sel(
            LATITUDE=point["Latitude"],
            LONGITUDE=point["Longitude"]
        ).to_series()

        for date, value in series.items():
            if pd.notna(value):
                records.append({
                    "Date": date,
                    "State": point["State"],
                    "District": point["District"],
                    "Rainfall_mm": float(value)
                })

    rainfall_df = pd.DataFrame(records)

    # Summarize grid-cell rainfall within each district per day
    daily = rainfall_df.groupby(
        ["Date", "State", "District"], as_index=False
    ).agg(
        Mean_Rainfall_mm=("Rainfall_mm", "mean"),
        Max_Rainfall_mm=("Rainfall_mm", "max"),
        Grid_Cells=("Rainfall_mm", "count")
    )

    daily.to_csv("district_daily_rainfall_2023.csv", index=False)

    print("\n===== DISTRICT RAINFALL SUMMARY =====")
    print("Rows:", len(daily))
    print("Districts:", daily["District"].nunique())
    print("Dates:", daily["Date"].nunique())
    print("Missing mean rainfall:", daily["Mean_Rainfall_mm"].isna().sum())
    print("\nFirst 10 rows:")
    print(daily.head(10).to_string(index=False))

    print("\nSaved as district_daily_rainfall_2023.csv")
