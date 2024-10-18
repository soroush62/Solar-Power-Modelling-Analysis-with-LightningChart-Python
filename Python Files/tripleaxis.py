import pandas as pd
import numpy as np
import lightningchart as lc
from datetime import datetime

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/Sonar.csv'
data = pd.read_csv(file_path)
data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])

daily_avg_power = data.groupby('Date')['Power Generated'].mean()
daily_avg_wind_speed = data.groupby('Date')['Average Wind Speed (Day)'].mean()
daily_avg_pressure = data.groupby('Date')['Average Barometric Pressure (Period)'].mean()

timestamps = [int(date.timestamp() * 1000) for date in daily_avg_power.index]

chart = lc.ChartXY(theme=lc.Themes.Dark, title="Power, Wind Speed, and Barometric Pressure Trends Over Time")

y_axis_left = chart.get_default_y_axis()
y_axis_left.set_title("Average Power Generated (W)")

power_series = chart.add_point_line_series(y_axis=y_axis_left)
power_series.set_name("Average Power Generated")
power_series.set_line_color(lc.Color('cyan'))
power_series.set_point_shape('Triangle').set_point_size(6)
power_series.add(x=timestamps, y=daily_avg_power.values.tolist())

y_axis_right_1 = chart.add_y_axis(opposite=True)
y_axis_right_1.set_title("Average Wind Speed (m/s)")

wind_speed_series = chart.add_point_line_series(y_axis=y_axis_right_1)
wind_speed_series.set_name("Average Wind Speed")
wind_speed_series.set_line_color(lc.Color('lime'))
wind_speed_series.set_point_shape('Circle').set_point_size(6)
wind_speed_series.add(x=timestamps, y=daily_avg_wind_speed.values.tolist())

y_axis_right_2 = chart.add_y_axis(opposite=True)
y_axis_right_2.set_title("Average Barometric Pressure (hPa)")

pressure_series = chart.add_point_line_series(y_axis=y_axis_right_2)
pressure_series.set_name("Average Barometric Pressure")
pressure_series.set_line_color(lc.Color('orange'))
pressure_series.set_point_shape('Square').set_point_size(6)
pressure_series.add(x=timestamps, y=daily_avg_pressure.values.tolist())

x_axis = chart.get_default_x_axis()
x_axis.set_title("Date")
x_axis.set_tick_strategy("DateTime")

legend = chart.add_legend()
legend.add(power_series).add(wind_speed_series).add(pressure_series)
legend.set_margin(140)

chart.open()
