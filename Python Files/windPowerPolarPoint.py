import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv' 
df = pd.read_csv(file_path)

angles = df['Average Wind Direction (Day)'].astype(float).values 
power_generated = df['Power Generated'].astype(float).values 

chart = lc.PolarChart(theme=lc.Themes.Light, title="Wind Direction vs. Power Generation")

point_series = chart.add_point_series()

min_power, max_power = power_generated.min(), power_generated.max()

data_points = []

for i in range(len(angles)):
    angle = angles[i]
    amplitude = power_generated[i] 
    
    data_points.append({
        'angle': float(angle), 
        'amplitude': amplitude,
        # 'value': float(power_generated[i]) 
    })

colors=[
        {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
        {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
        {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
        {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
        {'value': max_power, 'color': lc.Color('red')}  # High power (red)
    ]
point_series.set_data(data_points)

point_series.set_palette_colors(
    steps=colors,
    look_up_property='y',
    interpolate=True,    
)
point_series.set_point_shape('circle').set_point_size(10)

chart.open()

