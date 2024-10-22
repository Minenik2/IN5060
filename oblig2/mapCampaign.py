import pandas as pd
import plotly.express as px

# Step 1: Load the CSV data
file_path = 'data/Latency Tests - Online Gaming - Active Measurements.csv'  # Adjust the path as needed
data = pd.read_csv(file_path)

# Step 2: Data preprocessing
# Rename columns to standard names for easier access if needed
data.columns = [col.strip() for col in data.columns]  # Remove any extra spaces in column names

# Remove rows with missing latitude, longitude, Round Trip Latency Median, Operator, or Campaign
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'Round Trip Latency Median', 'Operator', 'Campaign'])

# Convert latitude, longitude, and Round Trip Latency Median to numeric
data['GPS Lat'] = pd.to_numeric(data['GPS Lat'], errors='coerce')
data['GPS Long'] = pd.to_numeric(data['GPS Long'], errors='coerce')
data['Round Trip Latency Median'] = pd.to_numeric(data['Round Trip Latency Median'], errors='coerce')

# Drop any remaining rows where GPS coordinates, Round Trip Latency Median, or Operator could not be converted
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'Round Trip Latency Median'])

# data = data[data['Campaign'] != "Gaming_Campaign_20"]
# data = data[data['Campaign'] != "Gaming_Campaign_28"]

# data = data[data['Campaign'] != "Gaming_Campaign_26"]
# data = data[data['Campaign'] != "Gaming_Campaign_2"]
# data = data[data['Campaign'] != "Gaming_Campaign_12"]
# data = data[data['Campaign'] != "Gaming_Campaign_31"]
# data = data[data['Campaign'] != "Gaming_Campaign_24"]
# data = data[data['Campaign'] != "Gaming_Campaign_13"]

# Step 3: Group data by Operator and Campaign, and display statistics
operator_groups = data.groupby('Operator')

for operator, group in operator_groups:
    num_data_points = len(group)
    campaign_groups = group.groupby('Campaign')
    num_campaigns = len(campaign_groups)
    
    print(f"\nOperator: {operator}")
    print(f"Total data points: {num_data_points}")
    print(f"Number of campaigns: {num_campaigns}")
    
    # Print the number of data points in each campaign
    for campaign, campaign_group in campaign_groups:
        print(f"  Campaign: {campaign} - Data points: {len(campaign_group)}")

# Step 4: Create a separate scatter map for each operator
unique_operators = data['Operator'].unique()

maps = []
for operator in unique_operators:
    # Filter data for the current operator
    operator_data = data[data['Operator'] == operator]
    
    # Create a scatter map for the operator, coloring by Campaign
    fig = px.scatter_mapbox(
        operator_data,
        lat='GPS Lat',
        lon='GPS Long',
        color='Campaign',  # Use the Campaign for coloring
        color_discrete_sequence=px.colors.qualitative.Plotly,  # Use a qualitative color scale for distinct colors
        size=[3] * len(operator_data),  # Set a consistent size for all markers
        size_max=12,  # Adjust the max size
        zoom=10,
        opacity=0.6,
        title=f'Active Measurements Latency Tests - Campaigns - {operator}'
    )

    # Update the layout for map style and performance tweaks
    fig.update_layout(
        title=f'Active Measurements Latency Tests - Campaigns - {operator}',
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},  # Add margins for the title
        uirevision='constant'  # Prevent the map from resetting when interacting with it
    )
    
    # Add the map to the list
    maps.append((operator, fig))

# Step 5: Display all the maps
for operator, fig in maps:
    print(f"\nMap for operator: {operator}")
    fig.show()
