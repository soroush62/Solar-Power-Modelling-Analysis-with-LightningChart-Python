import pandas as pd
import lightningchart as lc
from datetime import datetime

lc.set_license('my-license-key')

file_path = 'Dataset/Sonar.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])
data = data[['Date', 'Month', 'First Hour of Period', 'Power Generated']]

monthly_hourly_data = data.groupby(['Month', 'First Hour of Period'])['Power Generated'].mean().unstack(fill_value=0)

dashboard = lc.Dashboard(rows=2, columns=1, theme=lc.Themes.Light)

daily_chart = dashboard.ChartXY(row_index=0, column_index=0, title="Monthly Trends in Power Generation (Hourly Breakdown)")
daily_chart.get_default_y_axis().set_title("Average Power Generated (W)")
daily_chart.get_default_x_axis().set_title("Hour of Day")
legend = daily_chart.add_legend()
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for month in range(1, 13):
    series = daily_chart.add_area_series()
    series.set_name(month_labels[month - 1])
    series.add(list(monthly_hourly_data.columns), monthly_hourly_data.loc[month].values)
    legend.add(series)

seasonal_chart = dashboard.ChartXY(row_index=1, column_index=0, title="Seasonal Trends in Power Generation (Monthly Breakdown)")
seasonal_chart.get_default_y_axis().set_title("Average Power Generated (W)")
seasonal_chart.get_default_x_axis().set_title("Month")

monthly_data = data.groupby('Month')['Power Generated'].mean()
monthly_series = seasonal_chart.add_area_series()
monthly_series.set_name("Monthly Average Power Generation")
monthly_series.add(list(monthly_data.index), monthly_data.values)

x_axis = seasonal_chart.get_default_x_axis().set_tick_strategy('Empty')    
for i, month_name in enumerate(month_labels, start=1):
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value(i)
    custom_tick.set_text(month_name)

dashboard.open()

