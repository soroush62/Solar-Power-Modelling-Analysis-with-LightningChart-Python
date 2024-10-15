import pandas as pd
import numpy as np
import lightningchart as lc

# Set your LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'Dataset/Sonar.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Filter to ensure the dataset has the necessary columns and remove any missing values
data = data[['Day of Year', 'First Hour of Period', 'Power Generated']].dropna()

# Pivot data to prepare for the heatmap
# Rows = Hours (0-23), Columns = Days (1-365), Values = Power Generated
heatmap_data = data.pivot_table(
    index='First Hour of Period', 
    columns='Day of Year', 
    values='Power Generated', 
    aggfunc='mean'
)

# Convert the heatmap data to a NumPy array and replace any NaN values with a fill value
heatmap_array = heatmap_data.to_numpy()
heatmap_array[np.isnan(heatmap_array)] = 0  # Replace NaN values with zero or another appropriate value

# Create a new chart
chart = lc.ChartXY(
    title='Hourly Power Generation Pattern (Heatmap)',
    theme=lc.Themes.Light
)

# Create the heatmap grid series
grid_size_x, grid_size_y = heatmap_array.shape
heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y,
)

# Set the start, end, and step positions based on heatmap dimensions
heatmap_series.set_start(x=1, y=0)                   # Days start from 1
heatmap_series.set_end(x=365, y=23)                  # Up to day 365 and hour 23
heatmap_series.set_step(x=1, y=1)                    # Each day and hour increments by 1
heatmap_series.set_intensity_interpolation(True)     # Enable intensity interpolation

# Populate heatmap data
heatmap_series.invalidate_intensity_values(heatmap_array.tolist())

# Define a custom color palette for the heatmap
min_val = np.nanmin(heatmap_array)
max_val = np.nanmax(heatmap_array)
palette_steps = [
    {"value": min_val, "color": lc.Color('blue')},
    {"value": (min_val + max_val) / 2, "color": lc.Color('green')},
    {"value": max_val, "color": lc.Color('red')}
]

# Apply the color palette to the heatmap
heatmap_series.set_palette_colors(
    steps=palette_steps,
    look_up_property='value',
    interpolate=True
)

# Configure X and Y axis titles
chart.get_default_x_axis().set_title('Day of Year')
chart.get_default_y_axis().set_title('Hour of Day')

# Add a legend for the intensity values
chart.add_legend(data=heatmap_series).set_title('Power Generated (W)')

# Open the chart
chart.open()
