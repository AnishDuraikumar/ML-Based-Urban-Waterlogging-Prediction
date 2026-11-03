
import xarray as xr

file_path = "RF25_ind2023_rfp25.nc"

with xr.open_dataset(file_path) as ds:
    print("===== DATASET DETAILS =====")
    print(ds)

    print("\n===== VARIABLES =====")
    for name, variable in ds.data_vars.items():
        print(
            f"Name: {name}, "
            f"Dimensions: {variable.dims}, "
            f"Units: {variable.attrs.get('units', 'not specified')}"
        )

    print("\n===== COORDINATES =====")
    for name, coordinate in ds.coords.items():
        print(f"{name}: {coordinate.values[:5]}")
        print("Total values:", coordinate.size)

