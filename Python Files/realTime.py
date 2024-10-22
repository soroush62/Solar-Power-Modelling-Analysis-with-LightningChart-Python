import lightningchart as lc
import pandas as pd
import numpy as np
import trimesh
import time
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

df = pd.read_csv('Dataset/sonar.csv')

features = [
    "Average Temperature (Day)",
    "Average Wind Direction (Day)",  
    "Average Wind Speed (Day)",
    "Relative Humidity",
    "Average Barometric Pressure (Period)",
    "First Hour of Period"
]
target = "Power Generated"

X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)

dashboard = lc.Dashboard(
    theme=lc.Themes.TurquoiseHexagon,
    rows=2,
    columns=3,
)

sun_chart = dashboard.Chart3D(column_index=1, row_index=0)
sun_chart.set_title("Dynamic Moving Sun")

sun_model = sun_chart.add_mesh_model()
sun_obj_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project12/source/sunn.obj'

solar_model = sun_chart.add_mesh_model()
solar_obj_path = 'D:/Computer Aplication/WorkPlacement/Projects/Project12/source/Solar Panel.obj'

sun_scene = trimesh.load(sun_obj_path)
sun_mesh = sun_scene.dump(concatenate=True) if isinstance(sun_scene, trimesh.Scene) else sun_scene

sun_vertices = sun_mesh.vertices.flatten().tolist()
sun_indices = sun_mesh.faces.flatten().tolist()
sun_normals = sun_mesh.vertex_normals.flatten().tolist()
sun_model.set_model_geometry(vertices=sun_vertices, indices=sun_indices, normals=sun_normals)

solar_scene = trimesh.load(solar_obj_path)
solar_mesh = solar_scene.dump(concatenate=True) if isinstance(solar_scene, trimesh.Scene) else solar_scene

solar_vertices = solar_mesh.vertices.flatten().tolist()
solar_indices = solar_mesh.faces.flatten().tolist()
solar_normals = solar_mesh.vertex_normals.flatten().tolist()
solar_model.set_model_geometry(vertices=solar_vertices, indices=solar_indices, normals=solar_normals)

sun_model.set_scale(0.0005).set_model_rotation(90, 0, 0)
sun_model.set_color(lc.Color('yellow'))

solar_model.set_model_location(0, -1, 0)
solar_model.set_scale(0.1).set_model_rotation(0, 180, 0)
solar_model.set_color(lc.Color('grey'))

polar_chart = dashboard.PolarChart(column_index=0, row_index=0)
polar_chart.set_title("Wind Direction and Speed Distribution")

sectors = 12 
annuli = 5   
heatmap_series = polar_chart.add_heatmap_series(sectors=sectors, annuli=annuli)
heatmap_series.set_highlight(1)

# Set up a color palette for wind speed intensity
heatmap_series.set_palette_colors(
    steps=[
        {'value': 0, 'color': lc.Color('blue')},     # Low intensity
        {'value': 5, 'color': lc.Color('green')},    # Medium intensity
        {'value': 10, 'color': lc.Color('yellow')},  # High intensity
        {'value': 15, 'color': lc.Color('red')},     # Very high intensity
    ],
    look_up_property='value',
    interpolate=True
)
heatmap_series.set_intensity_interpolation('bilinear')  
intensity_values = [[0] * sectors for _ in range(annuli)]

gauge_chart = dashboard.GaugeChart(column_index=2, row_index=0)
gauge_chart.set_title("Predicted Energy Generated")
gauge_chart.set_angle_interval(start=225, end=-45)
gauge_chart.set_interval(start=0, end=float(df[target].max()))
gauge_chart.set_value(0)  
gauge_chart.set_unit_label("(Watts)").set_unit_label_font(18,weight='bold')
gauge_chart.set_value_label_font(28,weight='bold')
gauge_chart.set_value_indicators([
    {'start': 0, 'end': 0.25 * float(df[target].max()), 'color': lc.Color('red')},
    {'start': 0.25 * float(df[target].max()), 'end': 0.5 * float(df[target].max()), 'color': lc.Color('orange')},
    {'start': 0.5 * float(df[target].max()), 'end': 0.75 * float(df[target].max()), 'color': lc.Color('yellow')},
    {'start': 0.75 * float(df[target].max()), 'end': float(df[target].max()), 'color': lc.Color('green')},
])
gauge_chart.set_bar_thickness(30)
gauge_chart.set_value_indicator_thickness(15)

line_chart = dashboard.ChartXY(column_index=0, row_index=1, column_span=3)
line_chart.set_title('Time-Series Analysis of Environmental Data')

line_chart.get_default_y_axis().dispose()
legend = line_chart.add_legend()

series_dict = {}
for i, feature in enumerate(features[:-1]): 
    axis_y = line_chart.add_y_axis(stack_index=i)
    axis_y.set_margins(15 if i > 0 else 0, 15 if i < len(features) - 2 else 0)
    series = line_chart.add_line_series(y_axis=axis_y, data_pattern='ProgressiveX')
    series.set_name(feature)
    legend.add(series)
    series_dict[feature] = series

def calculate_sun_position(hour):
    radius = 1.0 
    angle = math.pi * (1 - (hour / 24)) 

    x = radius * math.cos(angle) 
    y = radius * math.sin(angle) - 1 
    return x, y

def simulate_real_time_prediction():
    for hour in range(24):
        generated_data = {
            "Average Temperature (Day)": float(np.random.uniform(60, 100)),
            "Average Wind Direction (Day)": float(np.random.uniform(0, 360)), 
            "Average Wind Speed (Day)": float(np.random.uniform(0, 15)),       
            "Relative Humidity": float(np.random.uniform(20, 80)),
            "Average Barometric Pressure (Period)": float(np.random.uniform(28, 30)),
            "First Hour of Period": int(hour)  
        }

        input_data = pd.DataFrame([generated_data])
        predicted_power = float(model.predict(input_data)[0])  

        gauge_chart.set_value(predicted_power)

        x_position, y_position = calculate_sun_position(hour)
        sun_model.set_model_location(x_position, y_position, 0)

        wind_direction = generated_data["Average Wind Direction (Day)"]
        wind_intensity = generated_data["Average Wind Speed (Day)"]

        sector_index = int((wind_direction / 360) * sectors) % sectors
        annulus_index = min(int(wind_intensity // 3), annuli - 1)  

        intensity_values[annulus_index][sector_index] += wind_intensity
        heatmap_series.invalidate_intensity_values(intensity_values)

        for feature, series in series_dict.items():
            series.clear()  
            series.add(list(range(hour + 1)), [float(np.random.uniform(60, 100)) for _ in range(hour + 1)])

        time.sleep(2)  

dashboard.open(live=True)

simulate_real_time_prediction()