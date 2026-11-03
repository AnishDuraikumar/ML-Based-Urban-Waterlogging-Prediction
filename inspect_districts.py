
import pandas as pd

df = pd.read_csv("District_FloodedArea.csv")

print("===== DATASET SHAPE =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== FIRST 10 ROWS =====")
print(df.head(10).to_string(index=False))

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== SAMPLE UNIQUE VALUES =====")
for col in df.columns:
    if df[col].nunique() <= 20:
        print(f"\n{col}:")
        print(df[col].dropna().unique())
