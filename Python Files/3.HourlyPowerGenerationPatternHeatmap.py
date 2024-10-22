import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license('my-license-key')

file_path = 'Dataset/Sonar.csv'  
data = pd.read_csv(file_path)

data = data[['Day of Year', 'First Hour of Period', 'Power Generated']].dropna()

# Rows = Hours (0-23), Columns = Days (1-365), Values = Power Generated
heatmap_data = data.pivot_table(
    index='First Hour of Period', 
    columns='Day of Year', 
    values='Power Generated', 
    aggfunc='mean'
)

heatmap_array = heatmap_data.to_numpy()
heatmap_array[np.isnan(heatmap_array)] = 0  

chart = lc.ChartXY(
    title='Hourly Power Generation Pattern (Heatmap)',
    theme=lc.Themes.Light
)

grid_size_x, grid_size_y = heatmap_array.shape
heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y,
)

heatmap_series.set_start(x=1, y=0)               
heatmap_series.set_end(x=365, y=23)              
heatmap_series.set_step(x=1, y=1)                  
heatmap_series.set_intensity_interpolation(True)   

heatmap_series.invalidate_intensity_values(heatmap_array.tolist())

min_val = np.nanmin(heatmap_array)
max_val = np.nanmax(heatmap_array)
palette_steps = [
    {"value": min_val, "color": lc.Color('blue')},
    {"value": (min_val + max_val) / 2, "color": lc.Color('green')},
    {"value": max_val, "color": lc.Color('red')}
]

heatmap_series.set_palette_colors(
    steps=palette_steps,
    look_up_property='value',
    interpolate=True
)

chart.get_default_x_axis().set_title('Day of Year')
chart.get_default_y_axis().set_title('Hour of Day')

chart.add_legend(data=heatmap_series).set_title('Power Generated (W)')

chart.open()
