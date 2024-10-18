import lightningchart as lc
import pandas as pd
import numpy as np
from matplotlib import cm

file_path = 'Dataset/Sonar.csv' 
data = pd.read_csv(file_path)

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

monthly_data = data.groupby('Month')['Power Generated'].mean()

month_names = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]

max_power = monthly_data.max()
amplitudes = (monthly_data / max_power).tolist() 

colors = cm.viridis(np.linspace(0, 1, len(amplitudes)))

chart = lc.PolarChart(theme=lc.Themes.Light, title="Seasonal Power Generation Trends")
radial_axis = chart.get_radial_axis().set_title("Month").set_title_font(weight="bold", size=14)
 
radial_axis.set_division(12)
radial_axis.set_tick_labels([
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])
 
radial_axis.set_clockwise(True).set_north(0)

legend=chart.add_legend()
legend.set_margin(180)
for i, (month, amplitude) in enumerate(zip(monthly_data.index, amplitudes)):
    angle_start = i * 30
    angle_end = (i + 1) * 30
    color = lc.Color(int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255))

    sector = chart.add_sector()
    sector.set_name(month_names[i])
    sector.set_amplitude_start(0) 
    sector.set_amplitude_end(amplitude)  
    sector.set_angle_start(angle_start)
    sector.set_angle_end(angle_end)
    sector.set_color(color=color)
    sector.set_stroke(color=lc.Color('white'), thickness=1) 
    legend.add(sector)


chart.open()
