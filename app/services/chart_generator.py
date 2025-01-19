import math
import os
import json
from typing import Dict
import svgwrite
from svgpathtools import parse_path

# Load the theme from a JSON file.
# If the theme file does not exist, raises a FileNotFoundError.
def load_theme(theme_name: str) -> Dict:
    """
    Loads the theme from a JSON file located in the 'themes' directory.

    Args:
        - theme_name: The name of the theme to load.

    Returns:
        A dictionary containing the theme's settings.
    
    Raises:
        FileNotFoundError: If the specified theme file is not found.
    """
    # Get the theme file path
    theme_path = os.path.join(os.path.dirname(__file__), "..", "themes", f"{theme_name}.json")
    # If the theme file does not exist, raise a FileNotFoundError
    if not os.path.exists(theme_path):
        raise FileNotFoundError(f"Theme '{theme_name}' not found.")
    # Open the theme file and return its JSON content
    with open(theme_path, "r") as theme_file:
        return json.load(theme_file)

def calculate_y_ticks(max_value: float, target_ticks: int = 5) -> tuple[float, list[float]]:
    """Calculate appropriate y-axis ticks
    
    Args:
        max_value: The maximum value of the data
        target_ticks: The desired number of ticks
        
    Returns:
        tuple(nice_max, ticks): The adjusted maximum value and a list of ticks
    """
    if max_value <= 0:
        return 0, [0]
    
    # 找到合適的刻度單位
    magnitude = 10 ** math.floor(math.log10(max_value))
    possible_steps = [1, 2, 5, 10]
    
    for step in possible_steps:
        unit = step * magnitude / 10
        n = math.ceil(max_value / unit)
        if n <= target_ticks:
            nice_max = n * unit
            ticks = [i * unit for i in range(n + 1)]
            return nice_max, ticks
            
    # 如果上面都不合適，使用最後的單位
    unit = possible_steps[-1] * magnitude / 10
    n = math.ceil(max_value / unit)
    nice_max = n * unit
    ticks = [i * unit for i in range(n + 1)]
    return nice_max, ticks

# Creating Smooth Curve Functions
def create_smooth_path(data_points):
    if not data_points:
        return ""
    
    path = f"M {data_points[0][0]},{data_points[0][1]}"
    for i in range(1, len(data_points)):
        x0, y0 = data_points[i-1]
        x1, y1 = data_points[i]
        cp1x = x0 + (x1 - x0) / 3
        cp2x = x1 - (x1 - x0) / 3
        path += f" C {cp1x},{y0} {cp2x},{y1} {x1},{y1}"
    return path


# Generate a chart based on the provided traffic data and theme.
# Returns the chart as an SVG file response.
def generate_chart(profile_name: str, traffic_results: dict, theme_name: str, height: int, width: int, radius: int,
                  bg_color: str=None, clones_color: str=None, views_color: str=None, clones_point_color: str=None,
                  views_point_color: str=None, exclude_repos: list=None):
    """
    Generates a line chart showing GitHub repository traffic data (views and clones),
    and returns the chart as an SVG file.

    Args:
        - profile_name: The profile name to be displayed in the chart title.
        - traffic_results: A dictionary containing the traffic data (views and clones) for each date.
        - theme_name: The theme name to be applied to the chart.
        - bg_color: (Optional) A custom background color for the chart.
        - clones_color: (Optional) A custom clones stroke color for the chart.
        - views_color: (Optional) A custom views stroke color for the chart.
        - clones_point_color: Optional clones point color for the chart.
        - views_point_color: Optional views point color for the chart.
        - radius: Corner radius for the chart's rectangular background.
        - height: Height of the chart.
        - width: Width of the chart.
        - exclude_repos: Comma-separated list of repository names to exclude from the chart.

    Returns:
        A svg string representing the generated chart.
    """
    # Handling of excluded repos
    if exclude_repos:
        exclude_repos_list = exclude_repos.split(",") if "," in exclude_repos else [exclude_repos]
    else:
        exclude_repos_list = []
    
    # Handling Traffic Data
    traffic_data = {}
    for traffic in traffic_results:
        repo_name = list(traffic.keys())[0]
        if repo_name not in exclude_repos_list:
            traffic_values = list(traffic.values())[0]
            
            # Handling clones data
            for date in traffic_values["clones"]:
                date_str = date["timestamp"].split("T")[0]
                if date_str not in traffic_data:
                    traffic_data[date_str] = {"clones": 0, "views": 0}
                traffic_data[date_str]["clones"] += date["count"]
            
            # Handling views data
            for date in traffic_values["views"]:
                date_str = date["timestamp"].split("T")[0]
                if date_str not in traffic_data:
                    traffic_data[date_str] = {"clones": 0, "views": 0}
                traffic_data[date_str]["views"] += date["count"]
    
    # load theme
    theme = load_theme(theme_name)
    
    # prepare data
    sorted_dates = sorted(traffic_data.keys())
    dates = [date.split('-')[-1] for date in sorted_dates]
    clones = [traffic_data[date]["clones"] for date in sorted_dates]
    views = [traffic_data[date]["views"] for date in sorted_dates]
    
    # Setting Margins and Drawing Area
    margin = {'top': 60, 'right': 50, 'bottom': 80, 'left': 60}
    plot_width = width - margin['left'] - margin['right']
    plot_height = height - margin['top'] - margin['bottom']

    # color setting
    clones_color = theme["line_colors"]["clones"] if clones_color is None else f'#{clones_color}'
    views_color = theme["line_colors"]["views"] if views_color is None else f'#{views_color}'
    clones_point_color = theme["point_colors"]["clones"] if clones_point_color is None else f'#{clones_point_color}'
    views_point_color = theme["point_colors"]["views"] if views_point_color is None else f'#{views_point_color}'
    background_color = f"#{bg_color}" if bg_color else theme["background_color"]
    text_color = theme["text_color"]
    grid_color = theme["grid_color"]

    # If there is transparency, switch the color
    background_color_opacity = 1
    clones_color_opacity = 1
    views_color_opacity = 1
    clones_point_color_opacity = 1
    views_point_color_opacity = 1
    text_color_opacity = 1
    grid_color_opacity = 1

    if len(background_color) == 9:
        background_color, opacity = background_color[:7], background_color[7:]
        background_color_opacity = int(opacity, 16) / 255
    if len(clones_color) == 9:
        clones_color, opacity = clones_color[:7], clones_color[7:]
        clones_color_opacity = int(opacity, 16) / 255
    if len(views_color) == 9:
        views_color, opacity = views_color[:7], views_color[7:]
        views_color_opacity = int(opacity, 16) / 255
    if len(clones_point_color) == 9:
        clones_point_color, opacity = clones_point_color[:7], clones_point_color[7:]
        clones_point_color_opacity = int(opacity, 16) / 255
    if len(views_point_color) == 9:
        views_point_color, opacity = views_point_color[:7], views_point_color[7:]
        views_point_color_opacity = int(opacity, 16) / 255
    if len(text_color) == 9:
        text_color, opacity = text_color[:7], text_color[7:]
        text_color_opacity = int(opacity, 16) / 255
    if len(grid_color) == 9:
        grid_color, opacity = grid_color[:7], grid_color[7:]
        grid_color_opacity = int(opacity, 16) / 255
    
    # create SVG
    dwg = svgwrite.Drawing(size=(width, height))
    
    # add background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), rx=radius, ry=radius, fill=background_color, fill_opacity=background_color_opacity))
    
    # Calculation ratio
    max_value = max(max(clones), max(views)) if clones and views else 0
    y_scale = plot_height / (max_value if max_value > 0 else 1)
    x_step = plot_width / (len(dates) - 1) if len(dates) > 1 else plot_width
    
    # add Title
    dwg.add(dwg.text(
        f"{profile_name}'s Repo Traffic Stats",
        insert=(width/2, margin['top']/2),
        text_anchor="middle",
        fill=text_color,
        fill_opacity=text_color_opacity,
        style="font-size: 20px; font-family: Arial"
    ))
    
    # add axes
    dwg.add(dwg.line(
        start=(margin['left'], height-margin['bottom']),
        end=(width-margin['right'], height-margin['bottom']),
        stroke=grid_color,
        stroke_opacity=grid_color_opacity
    ))
    dwg.add(dwg.line(
        start=(margin['left'], margin['top']),
        end=(margin['left'], height-margin['bottom']),
        stroke=grid_color,
        stroke_opacity=grid_color_opacity
    ))

    nice_max, y_ticks = calculate_y_ticks(max_value)
    y_scale = plot_height / nice_max if nice_max > 0 else 1

    # Draw horizontal gridlines and y-axis scales.
    for y_value in y_ticks:
        y_pos = height - margin['bottom'] - y_value * y_scale
        
        # add horizontal grid lines
        dwg.add(dwg.line(
            start=(margin['left'], y_pos),
            end=(width - margin['right'], y_pos),
            stroke=grid_color,
            stroke_opacity=grid_color_opacity,
            stroke_width=1,
            stroke_dasharray="5,5",
            opacity=0.5
        ))
        
        # add y-axis scales
        dwg.add(dwg.text(
            str(int(y_value)),
            insert=(margin['left'] - 10, y_pos + 5),
            text_anchor="end",
            fill=text_color,
            fill_opacity=text_color_opacity,
            style="font-size: 12px; font-family: Arial"
        ))
    
    # Adding Vertical Gridlines
    for i, date in enumerate(dates):
        x = margin['left'] + i * x_step
        
        # add vertical grid lines
        dwg.add(dwg.line(
            start=(x, margin['top']),
            end=(x, height - margin['bottom']),
            stroke=grid_color,
            stroke_opacity=grid_color_opacity,
            stroke_width=1,
            stroke_dasharray="5,5",
            opacity=0.5
        ))
    
    # Drawing data lines
    for dataset, line_color, line_opacity, point_color, point_opacity in [
        (clones, clones_color, clones_color_opacity, clones_point_color, clones_point_color_opacity),
        (views, views_color, views_color_opacity, views_point_color, views_point_color_opacity)]:
        points = [(margin['left'] + i * x_step, 
                  height - margin['bottom'] - value * y_scale)
                 for i, value in enumerate(dataset)]
        
        path_data = create_smooth_path(points)
        path = parse_path(path_data)
        path_length = path.length()

        path_element = dwg.path(
            d=path_data,
            stroke=line_color,
            stroke_opacity=line_opacity,
            fill='none',
            stroke_width=4,
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_dasharray=str(path_length),
            stroke_dashoffset=str(path_length)
        )

        path_element.add(dwg.animate(
            attributeName="stroke-dashoffset",
            from_=str(path_length),
            to_="0",
            dur="2s",
            repeatCount="1",
            fill="freeze" 
        ))

        for point in points:
            x, y = point
            dwg.add(dwg.circle(
                center=(x, y),
                r=4,
                fill=point_color,
                fill_opacity=point_opacity
            ))
        
        dwg.add(path_element)
    
    # add x-axis tag
    for i, date in enumerate(dates):
        x = margin['left'] + i * x_step
        dwg.add(dwg.text(
            date,
            insert=(x, height-margin['bottom']+20),
            transform=f"rotate(45, {x}, {height-margin['bottom']+20})",
            fill=text_color,
            fill_opacity=text_color_opacity,
            style="font-size: 12px; font-family: Arial"
        ))
    
    # add x-axis title
    dwg.add(dwg.text(
        "Days",
        insert=(width/2, height-margin['bottom']/3),  # 改成 margin['bottom']/3
        text_anchor="middle",
        fill=text_color,
        fill_opacity=text_color_opacity,
        style="font-size: 14px; font-family: Arial"
    ))
    dwg.add(dwg.text(
        "Count",
        insert=(margin['left']/3, height/2),
        text_anchor="middle",
        transform=f"rotate(-90, {margin['left']/3}, {height/2})",
        fill=text_color,
        fill_opacity=text_color_opacity,
        style="font-size: 14px; font-family: Arial"
    ))
    
    # add lengend
    legend_offset = 15
    legend_y = height - margin['bottom']/3 + legend_offset 
    # Clones legend
    dwg.add(dwg.line(
        start=(width/2 - 60, legend_y),
        end=(width/2 - 40, legend_y),
        stroke=clones_color,
        stroke_opacity=clones_color_opacity,
        stroke_width=3
    ))
    dwg.add(dwg.text(
        "Clones",
        insert=(width/2 - 30, legend_y + 5),
        fill=text_color,
        fill_opacity=text_color_opacity,
        style="font-size: 12px; font-family: Arial"
    ))
    # Views legend
    dwg.add(dwg.line(
        start=(width/2 + 40, legend_y),
        end=(width/2 + 60, legend_y),
        stroke=views_color,
        stroke_opacity=views_color_opacity,
        stroke_width=3
    ))
    dwg.add(dwg.text(
        "Views",
        insert=(width/2 + 70, legend_y + 5),
        fill=text_color,
        fill_opacity=text_color_opacity,
        style="font-size: 12px; font-family: Arial"
    ))
    
    return dwg.tostring()