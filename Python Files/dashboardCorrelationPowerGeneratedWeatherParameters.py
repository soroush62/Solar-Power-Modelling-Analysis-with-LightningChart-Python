import pandas as pd
import numpy as np
import lightningchart as lc

# Load LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable2.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv'  # Update this path to the actual file path
data = pd.read_csv(file_path)

# Selecting relevant columns for plotting
variables = ["Average Temperature (Day)", "Average Wind Speed (Day)", "Sky Cover", 
             "Relative Humidity", "Average Barometric Pressure (Period)", "Power Generated"]

# Filtering the data to only include rows without NaN values in the selected columns
data = data[variables].dropna()

# Ensure all data is cast to Python-native types
data = data.astype({
    "Average Temperature (Day)": float,
    "Average Wind Speed (Day)": float,
    "Sky Cover": float,
    "Relative Humidity": float,
    "Average Barometric Pressure (Period)": float,
    "Power Generated": float
})

# Define color intensity range based on Power Generated values
min_power, max_power = data["Power Generated"].min(), data["Power Generated"].max()

# Define color gradient function (blue to red)
def get_color(value):
    # Normalize the power generation value between 0 and 1
    ratio = (value - min_power) / (max_power - min_power)
    # Define color gradient (0: blue, 1: red)
    r = int(255 * ratio)
    b = int(255 * (1 - ratio))
    return lc.Color(r, 0, b)

# Setting up the LightningChart Dashboard with one row and multiple columns
dashboard = lc.Dashboard(
    rows=1,
    columns=len(variables) - 1,
    theme=lc.Themes.Dark
)

# Function to create scatter charts with color intensity
def create_scatter_chart(dashboard, x_data, y_data, title, x_label, column_index):
    chart = dashboard.ChartXY(
        column_index=column_index,
        row_index=0
    )
    chart.set_title(title)
    chart.set_title_font(size=12)
    chart.set_padding(0)

    # Add scatter points with color intensity based on power generation
    for x, y, power in zip(x_data, y_data, data["Power Generated"]):
        color = get_color(power)  # Set color intensity based on Power Generated
        point_series = chart.add_point_series()  # Create a new series for each point
        point_series.add([float(x)], [float(y)])
        point_series.set_point_color(color).set_point_size(5)  # Apply the color

    chart.get_default_x_axis().set_title(x_label)
    chart.get_default_y_axis().set_title("Power Generated")

# Create scatter charts for each variable
for i, var in enumerate(variables[:-1]):
    x_data = data[var].values
    y_data = data["Power Generated"].values
    create_scatter_chart(dashboard, x_data, y_data, f'{var} vs Power Generated', var, i)

# Open the dashboard to view the charts
dashboard.open()
