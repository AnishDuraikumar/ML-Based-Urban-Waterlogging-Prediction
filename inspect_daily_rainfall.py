
import pandas as pd

file_path = "rainfall_districtwise_daily_imd.csv"

df = pd.read_csv(file_path)

print("===== DATASET SIZE =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== FIRST 10 ROWS =====")
print(df.head(10).to_string(index=False))

print("\n===== DATE COVERAGE =====")
for column in df.columns:
    if "date" in column.lower():
        dates = pd.to_datetime(df[column], errors="coerce")
        print("Date column:", column)
        print("Earliest:", dates.min())
        print("Latest:", dates.max())
        print("Rows with valid dates:", dates.notna().sum())

print("\n===== DISTRICT COLUMN CHECK =====")
for column in df.columns:
    if "district" in column.lower():
        print("District column:", column)
        print("Sample districts:")
        print(df[column].dropna().astype(str).unique()[:20])
