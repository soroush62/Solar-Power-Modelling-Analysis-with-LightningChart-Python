import lightningchart as lc
import pandas as pd
import numpy as np

file_path = 'Dataset/Sonar.csv' 
data = pd.read_csv(file_path)

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

corr_matrix = data.corr()

corr_array = corr_matrix.to_numpy()

labels = corr_matrix.columns

chart = lc.ChartXY(
    title="Correlation Heatmap",
    theme=lc.Themes.Dark
)

grid_size_x, grid_size_y = corr_array.shape

heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y,
)

heatmap_series.set_start(x=0, y=0)
heatmap_series.set_end(x=grid_size_x, y=grid_size_y)
heatmap_series.set_step(x=1, y=1)
heatmap_series.set_wireframe_stroke(thickness=1, color=lc.Color('white'))

heatmap_series.invalidate_intensity_values(corr_array.tolist())
heatmap_series.set_intensity_interpolation(False)

palette_steps = [
    {"value": 0, "color": lc.Color(51,0,51)},   # No correlation (black)
    {"value": 0.5, "color": lc.Color('red')},     # Moderate correlation (red)
    {"value": 1, "color": lc.Color('white')}     # Positive correlation (white)
]

heatmap_series.set_palette_colors(
    steps=palette_steps,
    look_up_property='value',
    interpolate=True
)

x_axis = chart.get_default_x_axis()
y_axis = chart.get_default_y_axis()

x_axis.set_tick_strategy('Empty')
y_axis.set_tick_strategy('Empty')

for i, label in enumerate(labels):
    custom_tick = x_axis.add_custom_tick().set_tick_label_rotation(45)
    custom_tick.set_value(i + 0.5) 
    custom_tick.set_text(label)


# Set custom labels for Y-axis
for i, label in enumerate(labels):
    custom_tick = y_axis.add_custom_tick()
    custom_tick.set_value(i + 0.5) 
    custom_tick.set_text(label)
chart.add_legend(data=heatmap_series).set_margin(-20)

chart.open()
