import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_file.csv' with the actual path to your CSV file
df = pd.read_csv(r'C:\Users\Rem\Desktop\in5060\Throughput Tests - Speedtest - Active Measurements.csv')

print(df.head())  # Shows the first 5 rows of the data

# Inspect the data to see if the 'RSRP' column exists
print(df.columns)

# Replace '?' with NaN in the 'RSRP' column
df['RSRP'].replace('?', pd.NA, inplace=True)

# Convert the column to numeric, forcing invalid parsing to NaN
df['RSRP'] = pd.to_numeric(df['RSRP'], errors='coerce')

# Forward fill the missing values (i.e., replace NaN with the previous valid value)
df['RSRP'].fillna(method='ffill', inplace=True)

print("WE REPLACED!")
print(df.head())  # Or check any specific rows

# Filter by the 'RSRP' column if it exists
rsrp_data = df['RSRP']

# Descriptive statistics
print(rsrp_data.describe())

#plt.hist(rsrp_data, bins=30, color='blue', edgecolor='black')
#plt.title('RSRP Data Distribution')
#plt.xlabel('RSRP Value')
#plt.ylabel('Frequency')
#plt.show()

# Assuming 'Time' is a column in your data
plt.plot(df['Time'], df['RSRP'])
plt.title('RSRP Over Time')
plt.xlabel('Time')
plt.ylabel('RSRP')
plt.show()

# Check for missing data
print(df.isnull().sum())

# Drop rows with missing values (if needed)
df = df.dropna()

plt.savefig('my_plot.png')