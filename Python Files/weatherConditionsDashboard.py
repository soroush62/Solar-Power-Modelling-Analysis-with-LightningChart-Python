import pandas as pd
import lightningchart as lc

# Load LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable2.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv'  # Update this path
data = pd.read_csv(file_path)

# Selecting relevant columns for plotting
data = data[['Day of Year', 'Average Temperature (Day)', 'Relative Humidity', 
             'Average Wind Speed (Day)', 'Sky Cover']].dropna()

# Initialize dashboard
dashboard = lc.Dashboard(
    rows=2,
    columns=2,
    theme=lc.Themes.Dark
)

# Define a function to create line charts
def create_line_chart(dashboard, row_index, column_index, title, x_values, y_values, y_axis_title, line_color):
    chart = dashboard.ChartXY(
        row_index=row_index,
        column_index=column_index
    )
    chart.set_title(title)
    chart.get_default_x_axis().set_title("Day of Year")
    chart.get_default_y_axis().set_title(y_axis_title)
    
    # Create line series
    line_series = chart.add_line_series()
    line_series.add(x_values, y_values)
    line_series.set_line_color(line_color)
    
    return chart

# Extracting x values for the 'Day of Year'
x_values = data['Day of Year'].tolist()

# Creating each subplot as a line chart within the dashboard
create_line_chart(
    dashboard, row_index=0, column_index=0, title="Average Temperature",
    x_values=x_values, y_values=data['Average Temperature (Day)'].tolist(),
    y_axis_title="Temperature (°F)", line_color=lc.Color(255, 0, 0)  # Red
)

create_line_chart(
    dashboard, row_index=0, column_index=1, title="Relative Humidity",
    x_values=x_values, y_values=data['Relative Humidity'].tolist(),
    y_axis_title="Humidity (%)", line_color=lc.Color(0, 0, 255)  # Blue
)

create_line_chart(
    dashboard, row_index=1, column_index=0, title="Average Wind Speed",
    x_values=x_values, y_values=data['Average Wind Speed (Day)'].tolist(),
    y_axis_title="Wind Speed (mph)", line_color=lc.Color(0, 255, 0)  # Green
)

create_line_chart(
    dashboard, row_index=1, column_index=1, title="Sky Cover",
    x_values=x_values, y_values=data['Sky Cover'].tolist(),
    y_axis_title="Sky Cover (0-10)", line_color=lc.Color(128, 0, 128)  # Purple
)

# Open the dashboard
dashboard.open()