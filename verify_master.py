import pandas as pd

df = pd.read_csv('master_indian_weather_dataset.csv')

print('='*60)
print('MASTER DATASET VERIFICATION')
print('='*60)
print(f'\nTotal Records: {len(df):,}')
print(f'Date Range: {df["date"].min()} to {df["date"].max()}')
print(f'Unique Locations: {df["location"].nunique()}')
print(f'\nTop 10 Locations by Record Count:')
print(df["location"].value_counts().head(10))
print(f'\nBasic Statistics:')
print(df.describe())
print(f'\nData Quality Check:')
print(f'Missing Values: {df.isna().sum().sum()}')
print(f'Duplicate Rows: {df.duplicated().sum()}')
