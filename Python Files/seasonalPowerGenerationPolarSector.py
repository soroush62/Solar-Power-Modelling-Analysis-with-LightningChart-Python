import lightningchart as lc
import pandas as pd
import numpy as np

# Load the license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Extract necessary columns
angles = df['Average Wind Direction (Day)'].astype(float).values 
power_generated = df['Power Generated'].astype(float).values 

# Create the Polar Chart
chart = lc.PolarChart(theme=lc.Themes.Light, title="Wind Direction vs. Power Generation")

# Add Polar Point Series to the chart
point_series = chart.add_point_series()

# Define color intensity based on power generated
min_power, max_power = power_generated.min(), power_generated.max()

# Set up data points for the series
data_points = []
for i in range(len(angles)):
    angle = angles[i]
    amplitude = power_generated[i] 
    data_points.append({
        'angle': float(angle), 
        'amplitude': amplitude,
    })

# Set data for the point series
point_series.set_data(data_points)

# Set color palette based on power generated
point_series.set_palette_colors(
    steps=[
        {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
        {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
        {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
        {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
        {'value': max_power, 'color': lc.Color('red')}  # High power (red)
    ],
    look_up_property='y',
    interpolate=True,    
)

# Set point shape and size
point_series.set_point_shape('circle').set_point_size(10)

# Use built-in Legend for the chart
legend = chart.add_legend()
legend.set_title('Power Intensity Levels (kW)')

# Adding multiple dummy series to the legend to show color ranges (simulated color legend)
for level, color_name, label in zip([min_power, max_power * 0.25, max_power * 0.5, max_power * 0.75, max_power], 
                                    ['purple', 'blue', 'green', 'yellow', 'red'],
                                    ['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High']):
    dummy_series = chart.add_point_series()
    dummy_series.set_point_color(lc.Color(color_name))
    dummy_series.set_name(f'{label}: {int(level)} kW')
    dummy_series.set_visible(False)  # We make the series invisible but keep them in the legend
    legend.add(dummy_series)

# Open the chart
chart.open()
