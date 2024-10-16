import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/Sonar.csv' 
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

monthly_data = []
for month, month_df in data.groupby('Month'):
    monthly_children = []
    for day, day_df in month_df.groupby('Day'):
        daily_children = []
        for hour, hour_df in day_df.groupby('First Hour of Period'):
            total_power_hour = int(hour_df['Power Generated'].sum()) 
            daily_children.append({'name': f'{hour}:00', 'value': total_power_hour})
        
        daily_total = sum(child['value'] for child in daily_children)
        monthly_children.append({'name': f'Day {day}', 'value': daily_total, 'children': daily_children})
    
    month_total = sum(child['value'] for child in monthly_children)
    monthly_data.append({'name': f'Month {month}', 'value': month_total, 'children': monthly_children})

chart = lc.TreeMapChart(
    theme=lc.Themes.Dark,
    title="Treemap of Power Generation by Month, Day, and Hour"
)

chart.set_data(monthly_data)

chart.open()
