import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable2.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/Sonar.csv'
data = pd.read_csv(file_path)

data = data[['Day of Year', 'Average Temperature (Day)', 'Relative Humidity', 
             'Average Wind Speed (Day)', 'Sky Cover']].dropna()

data = data.sort_values(by='Day of Year')

dashboard = lc.Dashboard(
    rows=2,
    columns=2,
    theme=lc.Themes.Dark
)

def create_line_chart(dashboard, row_index, column_index, title, x_values, y_values, y_axis_title, line_color):
    chart = dashboard.ChartXY(
        row_index=row_index,
        column_index=column_index
    )
    chart.set_title(title)
    chart.get_default_x_axis().set_title("Day of Year")
    chart.get_default_y_axis().set_title(y_axis_title)
    
    line_series = chart.add_line_series()
    line_series.add(x_values, y_values)
    line_series.set_line_color(line_color)
    
    return chart

def create_point_chart(dashboard, row_index, column_index, title, x_values, y_values, y_axis_title, point_color):
    chart = dashboard.ChartXY(
        row_index=row_index,
        column_index=column_index
    )
    chart.set_title(title)
    chart.get_default_x_axis().set_title("Day of Year")
    chart.get_default_y_axis().set_title(y_axis_title)
    
    point_series = chart.add_point_series()
    point_series.add(x_values, y_values)
    point_series.set_point_color(point_color)

    return chart

x_values = data['Day of Year'].tolist()

create_line_chart(
    dashboard, row_index=0, column_index=0, title="Average Temperature",
    x_values=x_values, y_values=data['Average Temperature (Day)'].tolist(),
    y_axis_title="Temperature (°F)", line_color=lc.Color(255, 0, 0)  # Red
)

create_line_chart(
    dashboard, row_index=0, column_index=1, title="Relative Humidity",
    x_values=x_values, y_values=data['Relative Humidity'].tolist(),
    y_axis_title="Humidity (%)", line_color=lc.Color('cyan')  # Cyan
)

create_line_chart(
    dashboard, row_index=1, column_index=0, title="Average Wind Speed",
    x_values=x_values, y_values=data['Average Wind Speed (Day)'].tolist(),
    y_axis_title="Wind Speed (mph)", line_color=lc.Color(0, 255, 0)  # Green
)

create_point_chart(
    dashboard, row_index=1, column_index=1, title="Sky Cover",
    x_values=x_values, y_values=data['Sky Cover'].tolist(),
    y_axis_title="Sky Cover (0-10)", point_color=lc.Color(128, 0, 128)  # Purple
)

dashboard.open()

