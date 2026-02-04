import pandas as pd

df = pd.read_csv('master_indian_weather_dataset.csv')

print('='*60)
print('IMPROVED MASTER DATASET')
print('='*60)
print(f'\nTotal Records: {len(df):,}')
print(f'\nColumns ({len(df.columns)}): {list(df.columns)}')
print(f'\nFirst 10 rows:')
print(df.head(10))
print(f'\nTemp Range Statistics:')
print(df['temp_range'].describe())
print(f'\nSample dates (showing date format):')
print(df['date'].head(5))
print(f'\nData types:')
print(df.dtypes)
