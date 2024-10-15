import pandas as pd
import numpy as np
import lightningchart as lc

# Load LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv'  # Replace this with the actual file path
data = pd.read_csv(file_path)

# Ensure the dataset has the necessary columns and filter out rows with missing data
data = data[['Day of Year', 'First Hour of Period', 'Power Generated']].dropna()

# Pivot data to prepare for the heatmap
heatmap_data = data.pivot_table(
    index='First Hour of Period', 
    columns='Day of Year', 
    values='Power Generated', 
    aggfunc='mean'
)

# Fill missing data (optional, if necessary for display consistency)
heatmap_data.fillna(0, inplace=True)

# Convert the pivot table to a list of lists for the heatmap
heatmap_values = heatmap_data.values.tolist()

# Calculate min, median, and max for dynamic palette scaling
min_value = np.min(heatmap_values)
median_value = np.percentile(heatmap_values, 50)  # Median
max_value = np.max(heatmap_values)

# Create the heatmap chart with LightningChart
heatmap_chart = lc.ChartXY(
    theme=lc.Themes.Dark,
    title='Hourly Power Generation Pattern (Heatmap)'
)

# Add HeatmapGridSeries to display the power generation values
heatmap_series = heatmap_chart.add_heatmap_grid_series(
    columns=len(heatmap_data.columns),
    rows=len(heatmap_data.index)
)

heatmap_series.hide_wireframe()
heatmap_series.set_intensity_interpolation(False)
heatmap_series.invalidate_intensity_values(heatmap_values)

# Define a dynamic color palette for the heatmap based on min, median, and max values
heatmap_series.set_palette_colors(
    steps=[
        {'value': min_value, 'color': lc.Color(0, 0, 255)},    # Blue for low values
        {'value': median_value, 'color': lc.Color(0, 255, 0)},  # Green for median values
        {'value': max_value, 'color': lc.Color(255, 0, 0)}     # Red for high values
    ],
    look_up_property='value',
    percentage_values=False
)

# Configure X and Y axes
x_axis = heatmap_chart.get_default_x_axis()
x_axis.set_title('Day of Year')
x_axis.set_interval(1, 365)

y_axis = heatmap_chart.get_default_y_axis()
y_axis.set_title('Hour of Day')
y_axis.set_interval(0, 23)

# Open the heatmap chart
heatmap_chart.open()
