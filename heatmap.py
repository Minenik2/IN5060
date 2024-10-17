import pandas as pd
import folium
from folium.plugins import HeatMap, FastMarkerCluster

# Step 1: Load the CSV data
file_path = '4G - Passive Measurements.csv'  # Adjust the path as needed
data = pd.read_csv(file_path)

# Step 2: Data preprocessing
# Remove rows with missing latitude or longitude
data = data.dropna(subset=['Latitude', 'Longitude'])

# Optional: Filter based on specific coverage metrics, for example DM_RS-RSRP
#data = data[data['DM_RS-RSRP'].notna()]

# Limit the dataset to the first 10,000 rows to speed up processing
# data = data.head(1000000)

# Step 3: Create a base map
# Center the map around the mean location in the dataset
mean_lat = data['Latitude'].mean()
mean_lon = data['Longitude'].mean()

coverage_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)

# Step 4: Create a heatmap layer
# Prepare data for the heatmap (latitude, longitude, and optionally intensity)
heat_data = []
total_rows = len(data)

for index, row in enumerate(data.itertuples(), 1):
    # Normalize the DM_RS-RSRP value to be between 0 and 1
    normalized_intensity = (row.RSRP - data['RSRP'].min()) / (data['RSRP'].max() - data['RSRP'].min())
    heat_data.append([row.Latitude, row.Longitude, normalized_intensity])
    
    # Print progress every 1000 rows or at the last row
    if index % 1000 == 0 or index == total_rows:
        print(f"Processing: {index / total_rows * 100:.2f}%")

# Step 5: Add the heatmap to the map
HeatMap(data=heat_data, radius=10, blur=15, max_zoom=1).add_to(coverage_map)

# Step 5: Save the map to an HTML file
output_file_path = 'coverage_heatmap.html'
coverage_map.save(output_file_path)

output_file_path