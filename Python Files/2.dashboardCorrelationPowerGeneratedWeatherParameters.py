import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license('my-license-key')

file_path = 'Dataset/Sonar.csv' 
data = pd.read_csv(file_path)

variables = ["Average Temperature (Day)", "Average Wind Speed (Day)", "Sky Cover", 
             "Relative Humidity", "Average Barometric Pressure (Period)", "Power Generated"]

data = data[variables].dropna()

data = data.astype({
    "Average Temperature (Day)": float,
    "Average Wind Speed (Day)": float,
    "Sky Cover": float,
    "Relative Humidity": float,
    "Average Barometric Pressure (Period)": float,
    "Power Generated": float
})

min_power, max_power = data["Power Generated"].min(), data["Power Generated"].max()

def get_color(value):
    ratio = (value - min_power) / (max_power - min_power)
    r = int(255 * ratio)
    b = int(255 * (1 - ratio))
    return lc.Color(r, 0, b)

dashboard = lc.Dashboard(
    rows=4,
    columns=3,
    theme=lc.Themes.Dark
)

def create_scatter_chart(dashboard, x_data, y_data, title, x_label, row_index, column_index, row_span, column_span):
    chart = dashboard.ChartXY(
        row_index=row_index,
        column_index=column_index
        ,row_span=row_span
        ,column_span=column_span
    )
    chart.set_title(title)
    chart.set_title_font(size=12)
    chart.set_padding(0)
    chart.set_cursor_mode("show-pointed")

    for x, y, power in zip(x_data, y_data, data["Power Generated"]):
        color = get_color(power)  
        point_series = chart.add_point_series()  
        point_series.add([float(x)], [float(y)])
        point_series.set_point_color(color).set_point_size(5)

    chart.get_default_x_axis().set_title(x_label)
    chart.get_default_y_axis().set_title("Power Generated")

row_vars = ["Average Temperature (Day)", "Average Wind Speed (Day)", 
            "Relative Humidity", "Average Barometric Pressure (Period)"]

for i, var in enumerate(row_vars):
    x_data = data[var].values
    y_data = data["Power Generated"].values
    create_scatter_chart(
        dashboard, x_data, y_data, f'{var} vs Power Generated', var, row_index=i, column_index=0, row_span=1, column_span=2
    )

x_data_sky = data["Sky Cover"].values
y_data_sky = data["Power Generated"].values
create_scatter_chart(
    dashboard, x_data_sky, y_data_sky, 'Sky Cover vs Power Generated', 'Sky Cover', row_index=0, column_index=2, row_span=4, column_span=1
)

dashboard.open()