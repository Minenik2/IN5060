import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the CSV file into a DataFrame
file_path = 'Latency Tests - Online Gaming - Active Measurements.csv'  # Replace with the actual file path
data = pd.read_csv(file_path)

# Replace "?" with NaN and forward fill to propagate previous row's values
data.replace("?", pd.NA, inplace=True)
data.fillna(method='ffill', inplace=True)

# Drop rows with missing 'Round Trip Latency Median' or 'Operator' data
data = data.dropna(subset=['Round Trip Latency Median', 'Operator'])

# Convert 'Date' and 'Time' columns to a single datetime column
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d.%m.%Y %H:%M:%S.%f')

# Extract the hour from the 'Datetime' column
data['Hour'] = data['Datetime'].dt.hour

# Convert 'Round Trip Latency Median' to numeric (just in case)
data['Round Trip Latency Median'] = pd.to_numeric(data['Round Trip Latency Median'], errors='coerce')

# Drop any rows with NaN values in 'Round Trip Latency Median' after conversion
data = data.dropna(subset=['Round Trip Latency Median'])

# Get the list of unique operators
operators = data['Operator'].unique()

# Create a distinct color palette
palette = sns.color_palette("Set3", n_colors=24)

# Create a violin plot and boxplot for each operator
for operator in operators:
    # Filter data for the current operator
    operator_data = data[data['Operator'] == operator]
    
    # Create the figure
    plt.figure(figsize=(16, 10))
    
    # Violin plot for detailed distribution
    sns.violinplot(x='Hour', y='Round Trip Latency Median', data=operator_data, palette=palette, inner=None, alpha=0.6)
    
    # Overlay the boxplot for central tendency and spread
    sns.boxplot(x='Hour', y='Round Trip Latency Median', data=operator_data, palette=palette, width=0.3, fliersize=0)
    
    # Title and labels
    plt.title(f'Latency Distribution by Hour of the Day for Operator {operator}')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Round Trip Latency Median (ms)')
    plt.xticks(range(0, 24))  # Set x-ticks to represent each hour
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Explanation of the plot components below the plot
    plt.figtext(0.15, -0.15, 'Plot Explanation:\n'
                             '- Violin plot shows the distribution of latency data.\n'
                             '- The boxplot (inside the violin) shows the median, IQR, and whiskers.\n'
                             '- Each color corresponds to a different hour of the day.',
                fontsize=10, bbox=dict(facecolor='white', alpha=0.7), ha='left')

    # Adjust layout to make room for the explanation
    plt.subplots_adjust(bottom=0.25)

    # Save the plot to a file
    output_file_path = f'latency_violin_boxplot_by_hour_{operator}.png'
    plt.savefig(output_file_path, bbox_inches='tight')
    
    # Display the plot
    plt.show()
    
    print(f"Latency plot for operator {operator} saved to {output_file_path}")