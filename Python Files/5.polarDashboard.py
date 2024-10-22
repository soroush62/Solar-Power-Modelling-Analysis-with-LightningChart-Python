# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from matplotlib import cm

# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_path = 'Dataset/Sonar.csv'  
# df = pd.read_csv(file_path)

# dashboard = lc.Dashboard(
#     theme=lc.Themes.Dark,
#     rows=2,
#     columns=2,
# )

# # --- Chart 1: Polar Area Series - Power Generated ---
# num_points = len(df)
# df['angle'] = np.linspace(0, 365, num_points) 
# df['amplitude'] = df['Power Generated'] / df['Power Generated'].max() * 10

# chart1 = dashboard.PolarChart(row_index=0, column_index=0)
# chart1.set_title("Daily Power Generated")
# chart1.get_amplitude_axis().set_title("Normalized Power Generated (1-10)").set_title_font(weight="bold", size=14)
# chart1.get_radial_axis().set_title("Day of the Year").set_title_font(weight="bold", size=14)

# area_series = chart1.add_area_series().set_name("Power Generation").set_highlight(10)
# area_series.set_data([{'angle': angle, 'amplitude': amp} for angle, amp in zip(df['angle'], df['amplitude'])])
# area_series.set_stroke(thickness=1, color=lc.Color('cyan'))

# # --- Chart 2: Power Generated Distribution by Sky Cover Level ---
# sky_cover_levels = [0, 1, 2, 3, 4]
# grouped_data = df.groupby('Sky Cover')['Power Generated'].mean().reindex(sky_cover_levels, fill_value=0)
# max_power = df['Power Generated'].max()
# normalized_power = grouped_data / max_power

# chart2 = dashboard.SpiderChart(row_index=0, column_index=1)
# chart2.set_title("Power Generated Distribution by Sky Cover Level")

# colors = {
#     0: lc.Color('blue'),
#     1: lc.Color('green'),
#     2: lc.Color('yellow'),
#     3: lc.Color('orange'),
#     4: lc.Color('red')
# }
# legend2 = chart2.add_legend()
# polygon_series = {}
# for level in sky_cover_levels:
#     polygon_series[level] = chart2.add_polygon_series()
#     polygon_series[level].add_polygon().set_geometry([
#         {'angle': i * (360 / 5), 'amplitude': normalized_power[level] * 100} for i in range(5)
#     ])
#     polygon_series[level].set_color(color=colors[level]).set_name(f'Sky Cover Level {level}')
#     legend2.add(polygon_series[level])

# # --- Chart 3: Wind Direction vs. Power Generation (Point Series) ---
# angles = df['Average Wind Direction (Day)'].astype(float).values 
# power_generated = df['Power Generated'].astype(float).values 

# chart3 = dashboard.PolarChart(row_index=1, column_index=0)
# chart3.set_title("Wind Direction vs. Power Generation")
# point_series = chart3.add_point_series()
# point_series.set_highlight(10)

# min_power, max_power = power_generated.min(), power_generated.max()

# data_points = []
# for i in range(len(angles)):
#     angle = angles[i]
#     amplitude = power_generated[i] 
#     data_points.append({
#         'angle': float(angle), 
#         'amplitude': amplitude,
#     })

# point_series.set_data(data_points)

# point_series.set_palette_colors(
#     steps=[
#         {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
#         {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
#         {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
#         {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
#         {'value': max_power, 'color': lc.Color('red')}  # High power (red)
#     ],
#     look_up_property='y',
#     interpolate=True,    
# )

# point_series.set_point_shape('circle').set_point_size(10)

# # Add a legend
# # legend3 = chart3.add_legend()
# # legend3.set_title('Power Intensity Levels (kW)')

# for level, color_name, label in zip([min_power, max_power * 0.25, max_power * 0.5, max_power * 0.75, max_power], 
#                                     ['purple', 'blue', 'green', 'yellow', 'red'],
#                                     ['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High']):
#     dummy_series = chart3.add_point_series()
#     dummy_series.set_point_color(lc.Color(color_name))
#     dummy_series.set_name(f'{label}: {int(level)} kW')
#     dummy_series.set_visible(False)
#     # legend3.add(dummy_series)

# # --- Chart 4: Seasonal Power Generation Trends (Replacing Previous Chart) ---

# monthly_data = df.groupby('Month')['Power Generated'].mean()

# month_names = ["January", "February", "March", "April", "May", "June", 
#                "July", "August", "September", "October", "November", "December"]

# max_power = monthly_data.max()
# amplitudes = (monthly_data / max_power).tolist() 

# colors = cm.viridis(np.linspace(0, 1, len(amplitudes)))

# chart4 = dashboard.PolarChart(row_index=1, column_index=1)
# chart4.set_title("Seasonal Power Generation Trends")

# radial_axis = chart4.get_radial_axis().set_title("Month").set_title_font(weight="bold", size=14)
# radial_axis.set_division(12)
# radial_axis.set_clockwise(True).set_north(0)
# radial_axis.set_tick_labels([
#     'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
# ])

# legend4 = chart4.add_legend()

# for i, (month, amplitude) in enumerate(zip(monthly_data.index, amplitudes)):
#     angle_start = i * 30
#     angle_end = (i + 1) * 30
#     color = lc.Color(int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255))

#     sector = chart4.add_sector()
#     sector.set_name(month_names[i])
#     sector.set_amplitude_start(0) 
#     sector.set_amplitude_end(amplitude)  
#     sector.set_angle_start(angle_start)
#     sector.set_angle_end(angle_end)
#     sector.set_color(color=color)
#     sector.set_stroke(color=lc.Color('white'), thickness=1)
#     legend4.add(sector)

# dashboard.open()







# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from matplotlib import cm

# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_path = 'Dataset/Sonar.csv'  
# df = pd.read_csv(file_path)

# dashboard = lc.Dashboard(
#     theme=lc.Themes.Dark,
#     rows=2,
#     columns=2,
# )

# # --- Chart 1: Polar Area Series - Power Generated ---
# num_points = len(df)
# df['angle'] = np.linspace(0, 365, num_points) 
# df['amplitude'] = df['Power Generated'] / df['Power Generated'].max() * 10

# chart1 = dashboard.PolarChart(row_index=0, column_index=0)
# chart1.set_title("Daily Power Generated")
# chart1.get_amplitude_axis().set_title("Normalized Power Generated (1-10)").set_title_font(weight="bold", size=14)
# chart1.get_radial_axis().set_title("Day of the Year").set_title_font(weight="bold", size=14)

# area_series = chart1.add_area_series().set_name("Power Generation").set_highlight(10)
# area_series.set_data([{'angle': angle, 'amplitude': amp} for angle, amp in zip(df['angle'], df['amplitude'])])
# area_series.set_stroke(thickness=1, color=lc.Color('cyan'))

# # --- Chart 2: Sunny vs. Cloudy Day Environmental Factors ---
# factors = ['Average Temperature (Day)', 'Average Wind Speed (Day)', 'Relative Humidity', 'Average Barometric Pressure (Period)']
# power_factor = 'Power Generated'

# sunny_day = df[df['Is Daylight'] == True].mean()  
# cloudy_day = df[df['Is Daylight'] == False].mean() 

# sunny_values = sunny_day[factors].values
# cloudy_values = cloudy_day[factors].values

# max_values = np.maximum(sunny_values.max(), cloudy_values.max())  
# sunny_normalized = sunny_values / max_values
# cloudy_normalized = cloudy_values / max_values

# sunny_power = sunny_day[power_factor] / df[power_factor].max() 
# cloudy_power = cloudy_day[power_factor] / df[power_factor].max()

# sunny_normalized = np.append(sunny_normalized, sunny_power)
# cloudy_normalized = np.append(cloudy_normalized, cloudy_power)

# factors.append('Power Generation')

# chart2 = dashboard.PolarChart(row_index=0, column_index=1)
# chart2.set_title("Sunny Day vs. Cloudy Day: Environmental Factors and Power Generation")

# polygon_series_sunny = chart2.add_polygon_series()
# polygon_sunny = polygon_series_sunny.add_polygon().set_geometry([
#     {'angle': i * (360 / len(factors)), 'amplitude': sunny_normalized[i] * 100} for i in range(len(factors))
# ])
# polygon_series_sunny.set_color(color=lc.Color('yellow')).set_name('Sunny Day')

# polygon_series_cloudy = chart2.add_polygon_series()
# polygon_cloudy = polygon_series_cloudy.add_polygon().set_geometry([
#     {'angle': i * (360 / len(factors)), 'amplitude': cloudy_normalized[i] * 100} for i in range(len(factors))
# ])
# polygon_series_cloudy.set_color(color=lc.Color('blue')).set_name('Cloudy Day')

# radial_axis = chart2.get_radial_axis().set_title("Temperature").set_title_rotation(45)
# radial_axis.set_division(5)
# radial_axis.set_tick_labels(['Temperature', 'Wind Speed', 'Humidity', 'Pressure', 'Power'])

# legend = chart2.add_legend()
# legend.add(polygon_series_sunny)
# legend.add(polygon_series_cloudy)

# # --- Chart 3: Wind Direction vs. Power Generation (Point Series) ---
# angles = df['Average Wind Direction (Day)'].astype(float).values 
# power_generated = df['Power Generated'].astype(float).values 

# chart3 = dashboard.PolarChart(row_index=1, column_index=0)
# chart3.set_title("Wind Direction vs. Power Generation")
# point_series = chart3.add_point_series()
# point_series.set_highlight(10)

# min_power, max_power = power_generated.min(), power_generated.max()

# data_points = []
# for i in range(len(angles)):
#     angle = angles[i]
#     amplitude = power_generated[i] 
#     data_points.append({
#         'angle': float(angle), 
#         'amplitude': amplitude,
#     })

# point_series.set_data(data_points)

# point_series.set_palette_colors(
#     steps=[
#         {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
#         {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
#         {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
#         {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
#         {'value': max_power, 'color': lc.Color('red')}  # High power (red)
#     ],
#     look_up_property='y',
#     interpolate=True,    
# )

# point_series.set_point_shape('circle').set_point_size(10)

# # --- Chart 4: Seasonal Power Generation Trends (Replacing Previous Chart) ---
# monthly_data = df.groupby('Month')['Power Generated'].mean()

# month_names = ["January", "February", "March", "April", "May", "June", 
#                "July", "August", "September", "October", "November", "December"]

# max_power = monthly_data.max()
# amplitudes = (monthly_data / max_power).tolist() 

# colors = cm.viridis(np.linspace(0, 1, len(amplitudes)))

# chart4 = dashboard.PolarChart(row_index=1, column_index=1)
# chart4.set_title("Seasonal Power Generation Trends")

# radial_axis = chart4.get_radial_axis().set_title("Month").set_title_font(weight="bold", size=14)
# radial_axis.set_division(12)
# radial_axis.set_clockwise(True).set_north(0)
# radial_axis.set_tick_labels([
#     'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
# ])

# legend4 = chart4.add_legend()

# for i, (month, amplitude) in enumerate(zip(monthly_data.index, amplitudes)):
#     angle_start = i * 30
#     angle_end = (i + 1) * 30
#     color = lc.Color(int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255))

#     sector = chart4.add_sector()
#     sector.set_name(month_names[i])
#     sector.set_amplitude_start(0) 
#     sector.set_amplitude_end(amplitude)  
#     sector.set_angle_start(angle_start)
#     sector.set_angle_end(angle_end)
#     sector.set_color(color=color)
#     sector.set_stroke(color=lc.Color('white'), thickness=1)
#     legend4.add(sector)

# dashboard.open()








# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from matplotlib import cm

# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_path = 'Dataset/Sonar.csv'  
# df = pd.read_csv(file_path)

# dashboard = lc.Dashboard(
#     theme=lc.Themes.Dark,
#     rows=2,
#     columns=2,
# )

# # --- Chart 1: Polar Area Series - Power Generated ---
# num_points = len(df)
# df['angle'] = np.linspace(0, 365, num_points) 
# df['amplitude'] = df['Power Generated'] / df['Power Generated'].max() * 10

# chart1 = dashboard.PolarChart(row_index=0, column_index=0)
# chart1.set_title("Daily Power Generated")
# chart1.get_amplitude_axis().set_title("Normalized Power Generated (1-10)").set_title_font(weight="bold", size=14)
# chart1.get_radial_axis().set_title("Day of the Year").set_title_font(weight="bold", size=14)

# area_series = chart1.add_area_series().set_name("Power Generation").set_highlight(10)
# area_series.set_data([{'angle': angle, 'amplitude': amp} for angle, amp in zip(df['angle'], df['amplitude'])])
# area_series.set_stroke(thickness=1, color=lc.Color('cyan'))

# # --- Chart 2: Sunny vs. Cloudy Day Environmental Factors ---
# factors = ['Average Temperature (Day)', 'Average Wind Speed (Day)', 'Relative Humidity', 'Average Barometric Pressure (Period)']
# power_factor = 'Power Generated'

# sunny_day = df[df['Is Daylight'] == True].mean()  
# cloudy_day = df[df['Is Daylight'] == False].mean() 

# sunny_values = sunny_day[factors].values
# cloudy_values = cloudy_day[factors].values

# max_values = np.maximum(sunny_values.max(), cloudy_values.max())  
# sunny_normalized = sunny_values / max_values
# cloudy_normalized = cloudy_values / max_values

# sunny_power = sunny_day[power_factor] / df[power_factor].max() 
# cloudy_power = cloudy_day[power_factor] / df[power_factor].max()

# sunny_normalized = np.append(sunny_normalized, sunny_power)
# cloudy_normalized = np.append(cloudy_normalized, cloudy_power)

# factors.append('Power Generation')

# chart2 = dashboard.SpiderChart(row_index=0, column_index=1)
# chart2.set_title("Sunny Day vs. Cloudy Day: Environmental Factors and Power Generation")

# series_1 = chart2.add_series()
# radar_sunny = series_1.add_points([
#     {'axis': factor[i], 'value': sunny_normalized[i] * 100} for i, factor in enumerate(factors)
# ])
# radar_sunny.set_fill_color(color=lc.Color('yellow')).set_name('Sunny Day')

# series_2 = chart2.add_series()
# radar_cloudy = series_2.add_points([
#     {'axis': factor[i], 'value': cloudy_normalized[i] * 100} for i, factor in enumerate(factors)
# ])
# radar_cloudy.set_fill_color(color=lc.Color('blue')).set_name('Cloudy Day')

# for factor in factors:
#     chart2.add_axis(factor)

# legend = chart2.add_legend()
# legend.add(series_1)
# legend.add(series_2)

# # --- Chart 3: Wind Direction vs. Power Generation (Point Series) ---
# angles = df['Average Wind Direction (Day)'].astype(float).values 
# power_generated = df['Power Generated'].astype(float).values 

# chart3 = dashboard.PolarChart(row_index=1, column_index=0)
# chart3.set_title("Wind Direction vs. Power Generation")
# point_series = chart3.add_point_series()
# point_series.set_highlight(10)

# min_power, max_power = power_generated.min(), power_generated.max()

# data_points = []
# for i in range(len(angles)):
#     angle = angles[i]
#     amplitude = power_generated[i] 
#     data_points.append({
#         'angle': float(angle), 
#         'amplitude': amplitude,
#     })

# point_series.set_data(data_points)

# point_series.set_palette_colors(
#     steps=[
#         {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
#         {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
#         {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
#         {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
#         {'value': max_power, 'color': lc.Color('red')}  # High power (red)
#     ],
#     look_up_property='y',
#     interpolate=True,    
# )

# point_series.set_point_shape('circle').set_point_size(10)

# # --- Chart 4: Seasonal Power Generation Trends (Replacing Previous Chart) ---
# monthly_data = df.groupby('Month')['Power Generated'].mean()

# month_names = ["January", "February", "March", "April", "May", "June", 
#                "July", "August", "September", "October", "November", "December"]

# max_power = monthly_data.max()
# amplitudes = (monthly_data / max_power).tolist() 

# colors = cm.viridis(np.linspace(0, 1, len(amplitudes)))

# chart4 = dashboard.PolarChart(row_index=1, column_index=1)
# chart4.set_title("Seasonal Power Generation Trends")

# radial_axis = chart4.get_radial_axis().set_title("Month").set_title_font(weight="bold", size=14)
# radial_axis.set_division(12)
# radial_axis.set_clockwise(True).set_north(0)
# radial_axis.set_tick_labels([
#     'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
# ])

# legend4 = chart4.add_legend()

# for i, (month, amplitude) in enumerate(zip(monthly_data.index, amplitudes)):
#     angle_start = i * 30
#     angle_end = (i + 1) * 30
#     color = lc.Color(int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255))

#     sector = chart4.add_sector()
#     sector.set_name(month_names[i])
#     sector.set_amplitude_start(0) 
#     sector.set_amplitude_end(amplitude)  
#     sector.set_angle_start(angle_start)
#     sector.set_angle_end(angle_end)
#     sector.set_color(color=color)
#     sector.set_stroke(color=lc.Color('white'), thickness=1)
#     legend4.add(sector)

# dashboard.open()





import lightningchart as lc
import pandas as pd
import numpy as np
from matplotlib import cm

# Load the license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/Sonar.csv'  
df = pd.read_csv(file_path)

dashboard = lc.Dashboard(
    theme=lc.Themes.Dark,
    rows=2,
    columns=2,
)

# --- Chart 1: Polar Area Series - Power Generated ---
num_points = len(df)
df['angle'] = np.linspace(0, 365, num_points)
df['amplitude'] = df['Power Generated'] / df['Power Generated'].max() * 10

chart1 = dashboard.PolarChart(row_index=0, column_index=0)
chart1.set_title("Daily Power Generated")
chart1.get_amplitude_axis().set_title("Normalized Power Generated (1-10)").set_title_font(weight="bold", size=14)
chart1.get_radial_axis().set_title("Day of the Year").set_title_font(weight="bold", size=14)

area_series = chart1.add_area_series().set_name("Power Generation").set_highlight(10)
area_series.set_data([{'angle': angle, 'amplitude': amp} for angle, amp in zip(df['angle'], df['amplitude'])])
area_series.set_stroke(thickness=1, color=lc.Color('cyan'))

# --- Chart 2: Sunny vs. Cloudy Day Environmental Factors (Radar/Spider Chart) ---
factors = ['Average Temperature (Day)', 'Average Wind Speed (Day)', 'Relative Humidity', 'Average Barometric Pressure (Period)']
power_factor = 'Power Generated'

sunny_day = df[df['Is Daylight'] == True].mean()  
cloudy_day = df[df['Is Daylight'] == False].mean() 

sunny_values = sunny_day[factors].values
cloudy_values = cloudy_day[factors].values

max_values = np.maximum(sunny_values.max(), cloudy_values.max())  
sunny_normalized = sunny_values / max_values
cloudy_normalized = cloudy_values / max_values

sunny_power = sunny_day[power_factor] / df[power_factor].max() 
cloudy_power = cloudy_day[power_factor] / df[power_factor].max()

sunny_normalized = np.append(sunny_normalized, sunny_power)
cloudy_normalized = np.append(cloudy_normalized, cloudy_power)

factors.append('Power Generation')

chart2 = dashboard.SpiderChart(row_index=0, column_index=1)
chart2.set_title("Sunny Day vs. Cloudy Day: Environmental Factors and Power Generation")
chart2.set_web_mode("circle")

for factor in factors:
    chart2.add_axis(factor)

series_1 = chart2.add_series()
series_1.add_points([{'axis': factors[i], 'value': sunny_normalized[i] * 100} for i in range(len(factors))])
series_1.set_fill_color(lc.Color('yellow')).set_name('Sunny Day')

series_2 = chart2.add_series()
series_2.add_points([{'axis': factors[i], 'value': cloudy_normalized[i] * 100} for i in range(len(factors))])
series_2.set_fill_color(lc.Color('blue')).set_name('Cloudy Day')

legend2 = chart2.add_legend()
legend2.add(series_1)
legend2.add(series_2)

# --- Remaining Charts (Same as original) ---

# --- Chart 3: Wind Direction vs. Power Generation (Point Series) ---
angles = df['Average Wind Direction (Day)'].astype(float).values 
power_generated = df['Power Generated'].astype(float).values 

chart3 = dashboard.PolarChart(row_index=1, column_index=0)
chart3.set_title("Wind Direction vs. Power Generation")
point_series = chart3.add_point_series()
point_series.set_highlight(10)

min_power, max_power = power_generated.min(), power_generated.max()

data_points = []
for i in range(len(angles)):
    angle = angles[i]
    amplitude = power_generated[i] 
    data_points.append({
        'angle': float(angle), 
        'amplitude': amplitude,
    })

point_series.set_data(data_points)

point_series.set_palette_colors(
    steps=[
        {'value': min_power, 'color': lc.Color('purple')},   # Low power (purple)
        {'value': (min_power + max_power) * 0.25, 'color': lc.Color('blue')},  # Medium-low (blue)
        {'value': (min_power + max_power) * 0.5, 'color': lc.Color('green')},  # Medium (green)
        {'value': (min_power + max_power) * 0.75, 'color': lc.Color('yellow')},  # Medium-high (yellow)
        {'value': max_power, 'color': lc.Color('red')}  # High power (red)
    ],
    look_up_property='y',
    interpolate=True,    
)

point_series.set_point_shape('circle').set_point_size(10)

# --- Chart 4: Seasonal Power Generation Trends ---
monthly_data = df.groupby('Month')['Power Generated'].mean()

month_names = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]

max_power = monthly_data.max()
amplitudes = (monthly_data / max_power).tolist() 

colors = cm.viridis(np.linspace(0, 1, len(amplitudes)))

chart4 = dashboard.PolarChart(row_index=1, column_index=1)
chart4.set_title("Seasonal Power Generation Trends")

radial_axis = chart4.get_radial_axis().set_title("Month").set_title_font(weight="bold", size=14)
radial_axis.set_division(12)
radial_axis.set_clockwise(True).set_north(0)
radial_axis.set_tick_labels([
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])

legend4 = chart4.add_legend()

for i, (month, amplitude) in enumerate(zip(monthly_data.index, amplitudes)):
    angle_start = i * 30
    angle_end = (i + 1) * 30
    color = lc.Color(int(colors[i][0] * 255), int(colors[i][1] * 255), int(colors[i][2] * 255))

    sector = chart4.add_sector()
    sector.set_name(month_names[i])
    sector.set_amplitude_start(0) 
    sector.set_amplitude_end(amplitude)  
    sector.set_angle_start(angle_start)
    sector.set_angle_end(angle_end)
    sector.set_color(color=color)
    sector.set_stroke(color=lc.Color('white'), thickness=1)
    legend4.add(sector)

dashboard.open()
