"""
PRODUCTION-READY DATASET MERGE SCRIPT
Merges Indian Weather Repository and Climate Dataset 2024-2025
"""

import pandas as pd
import numpy as np

# 1️⃣ Load both datasets
print("Loading datasets...")
df_repo = pd.read_csv("IndianWeatherRepository.csv")
df_climate = pd.read_csv("Indian_Climate_Dataset_2024_2025.csv")

print(f"Repository dataset shape: {df_repo.shape}")
print(f"Climate dataset shape: {df_climate.shape}")

# 2️⃣ Standardize column names
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

print("\nStandardizing column names...")
df_repo = clean_columns(df_repo)
df_climate = clean_columns(df_climate)

# 3️⃣ Rename columns to a COMMON SCHEMA
# Repository dataset mappings
rename_map_repo = {
    "location_name": "location",
    "last_updated": "date",
    "temperature_celsius": "avg_temperature",
    "precip_mm": "rainfall",
    "wind_kph": "wind_speed",
    "humidity": "humidity"
}

# Climate dataset mappings
rename_map_climate = {
    "date": "date",
    "city": "location",
    "temperature_max_(°c)": "max_temperature",
    "temperature_min_(°c)": "min_temperature",
    "temperature_avg_(°c)": "avg_temperature",
    "rainfall_(mm)": "rainfall",
    "wind_speed_(km/h)": "wind_speed",
    "humidity_(%)": "humidity"
}

df_repo.rename(columns=rename_map_repo, inplace=True)
df_climate.rename(columns=rename_map_climate, inplace=True)

# 4️⃣ Ensure mandatory columns exist in BOTH
required_columns = [
    "date",
    "location",
    "max_temperature",
    "min_temperature",
    "avg_temperature",
    "humidity",
    "rainfall",
    "wind_speed"
]

print("\nEnsuring required columns exist...")
for col in required_columns:
    if col not in df_repo.columns:
        df_repo[col] = np.nan
    if col not in df_climate.columns:
        df_climate[col] = np.nan

# 5️⃣ Select ONLY useful columns
df_repo = df_repo[required_columns]
df_climate = df_climate[required_columns]

# 6️⃣ Convert date properly
print("\nConverting dates...")
df_repo["date"] = pd.to_datetime(df_repo["date"], errors="coerce")
df_climate["date"] = pd.to_datetime(df_climate["date"], errors="coerce")

# 7️⃣ MERGE (Append rows)
print("\nMerging datasets...")
merged_df = pd.concat(
    [df_repo, df_climate],
    axis=0,
    ignore_index=True
)

# 8️⃣ Handle missing values
print("\nHandling missing values...")
numeric_cols = [
    "max_temperature",
    "min_temperature",
    "avg_temperature",
    "humidity",
    "rainfall",
    "wind_speed"
]

for col in numeric_cols:
    merged_df[col] = merged_df[col].fillna(merged_df[col].median())

merged_df.dropna(subset=["date", "location"], inplace=True)

# 🔧 FIX 1: Normalize date (remove time component)
print("\nNormalizing dates (removing time component)...")
merged_df["date"] = pd.to_datetime(merged_df["date"]).dt.date

# 🔧 FIX 2: Add state column
print("\nAdding state column...")
merged_df["state"] = "India"

# ⭐ ENHANCEMENT: Add derived features
print("\nAdding derived features...")
merged_df["temp_range"] = merged_df["max_temperature"] - merged_df["min_temperature"]

# Reorder columns for better presentation
merged_df = merged_df[[
    "date",
    "location",
    "state",
    "max_temperature",
    "min_temperature",
    "avg_temperature",
    "temp_range",
    "humidity",
    "rainfall",
    "wind_speed"
]]

# 9️⃣ Final sanity check
print("\n" + "="*60)
print("FINAL MASTER DATASET")
print("="*60)
print(f"\nShape: {merged_df.shape}")
print(f"\nFirst 5 rows:")
print(merged_df.head())
print(f"\nMissing values:")
print(merged_df.isna().sum())
print(f"\nData types:")
print(merged_df.dtypes)

# 🔟 Save MASTER DATASET
output_file = "master_indian_weather_dataset.csv"
merged_df.to_csv(output_file, index=False)
print(f"\n✅ SUCCESS! Master dataset saved to: {output_file}")
print(f"Total records: {len(merged_df):,}")
