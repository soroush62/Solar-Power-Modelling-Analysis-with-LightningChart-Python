# import lightningchart as lc
# import pandas as pd
# import numpy as np

# # Load the license key
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the dataset
# file_path = 'Dataset/Sonar.csv'  # Replace with your actual file path
# df = pd.read_csv(file_path)

# # Extract necessary columns (angles represent hours in this case)
# angles = df['First Hour of Period'].astype(float).values * 15  # Scale hours to fit 360 degrees (24 hours)

# # Environmental factors as amplitudes
# average_temperature = df['Average Temperature (Day)'].astype(float).values
# wind_speed = df['Average Wind Speed (Day)'].astype(float).values
# humidity = df['Relative Humidity'].astype(float).values

# # Create the polar chart
# chart = lc.PolarChart(theme=lc.Themes.Light, title="Cyclic Environmental Factors")

# # Define and add the polygon for Average Temperature (Blue)
# polygon_series1 = chart.add_polygon_series()
# polygon1 = polygon_series1.add_polygon().set_geometry([
#     {'angle': angles[i], 'amplitude': average_temperature[i]} for i in range(len(angles))
# ])
# polygon_series1.set_color(color=lc.Color('blue')).set_name('Average Temperature')

# # Define and add the polygon for Wind Speed (Orange)
# polygon_series2 = chart.add_polygon_series()
# polygon2 = polygon_series2.add_polygon().set_geometry([
#     {'angle': angles[i], 'amplitude': wind_speed[i]} for i in range(len(angles))
# ])
# polygon_series2.set_color(color=lc.Color('orange')).set_name('Wind Speed')

# # Define and add the polygon for Relative Humidity (Yellow)
# polygon_series3 = chart.add_polygon_series()
# polygon3 = polygon_series3.add_polygon().set_geometry([
#     {'angle': angles[i], 'amplitude': humidity[i]} for i in range(len(angles))
# ])
# polygon_series3.set_color(color=lc.Color('yellow')).set_name('Relative Humidity')

# # Add Legend to display series names
# legend = chart.add_legend()
# legend.add(polygon_series1).add(polygon_series2).add(polygon_series3)
# # Open the chart
# chart.open()





import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/Sonar.csv'
df = pd.read_csv(file_path)

sky_cover_levels = [0, 1, 2, 3, 4]
grouped_data = df.groupby('Sky Cover')['Power Generated'].mean().reindex(sky_cover_levels, fill_value=0)

max_power = df['Power Generated'].max()
normalized_power = grouped_data / max_power

chart = lc.PolarChart(theme=lc.Themes.Light, title="Power Generated Distribution by Sky Cover Level")

colors = {
    0: lc.Color('blue'),
    1: lc.Color('green'),
    2: lc.Color('yellow'),
    3: lc.Color('orange'),
    4: lc.Color('red')
}
legend = chart.add_legend()
polygon_series = {}
for level in sky_cover_levels:
    polygon_series[level] = chart.add_polygon_series()
    polygon_series[level].add_polygon().set_geometry([
        {'angle': i * (360 / 5), 'amplitude': normalized_power[level] * 100} for i in range(5)
    ])
    polygon_series[level].set_color(color=colors[level]).set_name(f'Sky Cover Level {level}')
    legend.add(polygon_series[level])

chart.open()
