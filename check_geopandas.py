
import geopandas as gpd

gdf = gpd.read_file("india_district.geojson")

print("===== BOUNDARY DATA SUMMARY =====")
print("Number of features:", len(gdf))
print("Coordinate system:", gdf.crs)
print("Columns:", gdf.columns.tolist())

print("\n===== DISTRICT NAME SAMPLE =====")
print(gdf[["NAME_1", "NAME_2"]].head(10).to_string(index=False))

print("\n===== BOUNDS =====")
print(gdf.total_bounds)
