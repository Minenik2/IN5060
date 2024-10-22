import pandas as pd
from scipy.stats import kruskal
import scikit_posthocs as sp

# Load the CSV file into a DataFrame
file_path = 'data/Latency Tests - Online Gaming - Active Measurements.csv'  # Replace with the actual file path
data = pd.read_csv(file_path)

# Step 2: Data preprocessing
# Rename columns to standard names for easier access if needed
data.columns = [col.strip() for col in data.columns]  # Remove any extra spaces in column names

# Remove rows with missing latitude, longitude, Round Trip Latency Median, or Operator
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'Round Trip Latency Median', 'Operator', 'Campaign'])

# Convert latitude, longitude, and Round Trip Latency Median to numeric
data['GPS Lat'] = pd.to_numeric(data['GPS Lat'], errors='coerce')
data['GPS Long'] = pd.to_numeric(data['GPS Long'], errors='coerce')
data['Round Trip Latency Median'] = pd.to_numeric(data['Round Trip Latency Median'], errors='coerce')

# Drop any remaining rows where GPS coordinates, Round Trip Latency Median, or Operator could not be converted
data = data.dropna(subset=['GPS Lat', 'GPS Long', 'Round Trip Latency Median'])

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

# Perform the Kruskal-Wallis H-test
operators = data['Operator'].unique()
latency_data = [data[data['Operator'] == operator]['Round Trip Latency Median'].values for operator in operators]
stat, p_value = kruskal(*latency_data)

print(f'Kruskal-Wallis H-test statistic: {stat:.3f}')
print(f'p-value: {p_value}')

if p_value < 0.05:
    print("There is a significant difference in latency between at least two operators.")
    
    # Perform Dunn's test for post-hoc pairwise comparisons
    dunn_results = sp.posthoc_dunn(data, val_col='Round Trip Latency Median', group_col='Operator', p_adjust='bonferroni')
    
    # Display the results of Dunn's test
    print("Dunn's test pairwise comparisons (p-values):")
    print(dunn_results)

    # Determine which operator has the lowest median
    median_latencies = data.groupby('Operator')['Round Trip Latency Median'].median()
    best_operator = median_latencies.idxmin()
    print(f"The operator with the best latency (lowest median) is: {best_operator} with a median latency of {median_latencies.min()}")
    print(median_latencies)
else:
    print("There is no significant difference in latency between the operators.")
