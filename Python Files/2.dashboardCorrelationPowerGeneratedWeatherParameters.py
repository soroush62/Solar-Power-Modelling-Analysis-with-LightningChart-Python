import pandas as pd
import numpy as np
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable2.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

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
    rows=1,
    columns=len(variables) - 1,
    theme=lc.Themes.Dark
)

def create_scatter_chart(dashboard, x_data, y_data, title, x_label, column_index):
    chart = dashboard.ChartXY(
        column_index=column_index,
        row_index=0
    )
    chart.set_title(title)
    chart.set_title_font(size=12)
    chart.set_padding(0)

    for x, y, power in zip(x_data, y_data, data["Power Generated"]):
        color = get_color(power)  
        point_series = chart.add_point_series()  
        point_series.add([float(x)], [float(y)])
        point_series.set_point_color(color).set_point_size(5)
        

    chart.get_default_x_axis().set_title(x_label)
    chart.get_default_y_axis().set_title("Power Generated")

for i, var in enumerate(variables[:-1]):
    x_data = data[var].values
    y_data = data["Power Generated"].values
    create_scatter_chart(dashboard, x_data, y_data, f'{var} vs Power Generated', var, i)

dashboard.open()
