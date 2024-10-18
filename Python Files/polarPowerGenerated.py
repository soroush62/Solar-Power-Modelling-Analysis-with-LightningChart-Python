import lightningchart as lc
import pandas as pd
import numpy as np

file_path = 'Dataset/Sonar.csv'  
data = pd.read_csv(file_path)

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

num_points = len(data)
data['angle'] = np.linspace(0, 365, num_points) 
data['amplitude'] = data['Power Generated'] / data['Power Generated'].max() * 10

chart = lc.PolarChart(
    title="Polar Area Series - Power Generated",
    theme=lc.Themes.Light,
)
chart.get_amplitude_axis().set_title("Normalized Power Generated (1-10)").set_title_font(weight="bold", size=14)
chart.get_radial_axis().set_title("Day of the Year").set_title_font(weight="bold", size=14)

area_series = chart.add_area_series().set_name("Power Generation")
area_series.set_data([{'angle': angle, 'amplitude': amp} for angle, amp in zip(data['angle'], data['amplitude'])])
area_series.set_highlight(10)
line_series = chart.add_sector()

chart.open()
