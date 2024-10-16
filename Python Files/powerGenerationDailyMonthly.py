import pandas as pd
import lightningchart as lc
from datetime import datetime

# Set your LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'Dataset/Sonar.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Convert necessary columns to datetime and filter the required columns
data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])
data = data[['Date', 'Month', 'First Hour of Period', 'Power Generated']]

# Group data for daily trends (average power generated by hour of the day)
hourly_data = data.groupby(['Date', 'First Hour of Period'])['Power Generated'].mean().unstack(fill_value=0)

# Group data for seasonal trends (average power generated by month)
monthly_data = data.groupby(['Month'])['Power Generated'].mean()

# Initialize the dashboard
dashboard = lc.Dashboard(rows=2, columns=1, theme=lc.Themes.Light)

# Create Daily Trends Chart
daily_chart = dashboard.ChartXY(row_index=0, column_index=0, title="Daily Trends in Power Generation (Hourly Breakdown)")
daily_chart.get_default_y_axis().set_title("Average Power Generated (W)")
daily_chart.get_default_x_axis().set_title("Hour of Day")

# Create series for each day in daily trends
for date in hourly_data.index:
    series = daily_chart.add_area_series()
    series.set_name(date.strftime("%Y-%m-%d"))  # Set date as legend name
    series.add(list(hourly_data.columns), hourly_data.loc[date].values)

# Create Seasonal Trends Chart
seasonal_chart = dashboard.ChartXY(row_index=1, column_index=0, title="Seasonal Trends in Power Generation (Monthly Breakdown)")
seasonal_chart.get_default_y_axis().set_title("Average Power Generated (W)")
seasonal_chart.get_default_x_axis().set_title("Month")

# Adding filled line series for monthly data
monthly_series = seasonal_chart.add_area_series()
monthly_series.set_name("Monthly Average Power Generation")
monthly_series.add(list(monthly_data.index), monthly_data.values)

# Customize X-axis for month names
x_axis=seasonal_chart.get_default_x_axis().set_tick_strategy('Empty')    
month_labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for i, month_name in enumerate(month_labels, start=1):
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value(i)
    custom_tick.set_text(month_name)

dashboard.open()
