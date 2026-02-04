import pandas as pd

# Load dataset
df = pd.read_csv('master_indian_weather_dataset.csv')

# Convert date to standard string format for Excel
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Save back
df.to_csv('master_indian_weather_dataset.csv', index=False)

print('✓ Date format fixed for Excel compatibility')
print(f'Format: YYYY-MM-DD')
print(f'Sample dates: {df["date"].head(5).tolist()}')
print(f'\nNow reopen the CSV in Excel - dates will display properly!')
