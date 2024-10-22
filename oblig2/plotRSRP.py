import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file into a DataFrame
file_path = 'data/Latency Tests - Online Gaming - Active Measurements.csv'  # Replace with the actual file path
data = pd.read_csv(file_path)

# Step 2: Data preprocessing
# Rename columns to standard names for easier access if needed
data.columns = [col.strip() for col in data.columns]  # Remove any extra spaces in column names

# Remove rows with missing latitude, longitude, RSRP, or Operator
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'RSRP', 'Operator', 'Campaign'])

# Convert latitude, longitude, and RSRP to numeric
data['GPS Lat'] = pd.to_numeric(data['GPS Lat'], errors='coerce')
data['GPS Long'] = pd.to_numeric(data['GPS Long'], errors='coerce')
data['RSRP'] = pd.to_numeric(data['RSRP'], errors='coerce')

# Drop any remaining rows where GPS coordinates, RSRP, or Operator could not be converted
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'RSRP'])

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

data = data[data['Campaign'] != "Gaming_Campaign_20"]
data = data[data['Campaign'] != "Gaming_Campaign_28"]

data = data[data['Campaign'] != "Gaming_Campaign_26"]
data = data[data['Campaign'] != "Gaming_Campaign_2"]
data = data[data['Campaign'] != "Gaming_Campaign_12"]
data = data[data['Campaign'] != "Gaming_Campaign_31"]
data = data[data['Campaign'] != "Gaming_Campaign_24"]
data = data[data['Campaign'] != "Gaming_Campaign_13"]

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

data = data[data['Campaign'] != "Gaming_Campaign_20"]
data = data[data['Campaign'] != "Gaming_Campaign_28"]

data = data[data['Campaign'] != "Gaming_Campaign_26"]
data = data[data['Campaign'] != "Gaming_Campaign_2"]
data = data[data['Campaign'] != "Gaming_Campaign_12"]
data = data[data['Campaign'] != "Gaming_Campaign_31"]
data = data[data['Campaign'] != "Gaming_Campaign_24"]
data = data[data['Campaign'] != "Gaming_Campaign_13"]

# Convert 'RSRP' to numeric (just in case)
data['RSRP'] = pd.to_numeric(data['RSRP'], errors='coerce')

# Get the list of unique operators
operators = data['Operator'].unique()

# Create a distinct color palette
palette = sns.color_palette("Set3", n_colors=len(data['Campaign'].unique()))

# Create a violin plot and boxplot for each operator grouped by campaign
for operator in operators:
    # Filter data for the current operator
    operator_data = data[data['Operator'] == operator]
    
    # Create the figure
    plt.figure(figsize=(12, 6))
    
    # Violin plot for detailed distribution
    sns.violinplot(x='Campaign', y='RSRP', data=operator_data, palette=palette, inner=None, alpha=0.6)
    
    # Overlay the boxplot for central tendency and spread
    sns.boxplot(x='Campaign', y='RSRP', data=operator_data, palette='dark:.3', width=0.3, fliersize=0)
    
    # Title and labels
    plt.title(f'RSRP by Campaign for Operator {operator}')
    plt.xlabel('Campaign')
    plt.ylabel('RSRP (ms)')
    plt.xticks(rotation=45)  # Rotate x-ticks for better visibility
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.ylim(-135, -45)  # Adjust y-limit as needed

    # Save the plot to a file
    output_file_path = f'output/RSRP_violin_boxplot_by_campaign_{operator}.png'
    plt.savefig(output_file_path, bbox_inches='tight')
    
    # Display the plot
    plt.show()
    
    print(f"RSRP plot for operator {operator} saved to {output_file_path}")
