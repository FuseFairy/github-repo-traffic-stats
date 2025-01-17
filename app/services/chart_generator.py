import os
import json
import pygal
from typing import Dict
from pygal.style import Style

# Load the theme from a JSON file.
# If the theme file does not exist, raises a FileNotFoundError.
def load_theme(theme_name: str) -> Dict:
    """
    Loads the theme from a JSON file located in the 'themes' directory.

    Args:
        theme_name: The name of the theme to load.

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

# Generate a chart based on the provided traffic data and theme.
# Returns the chart as an SVG file response.
def generate_chart(profile_name: str, traffic_data: dict, theme_name: str, height: int, width: int, bg_color: str=None):
    """
    Generates a line chart showing GitHub repository traffic data (views and clones),
    and returns the chart as an SVG file.

    Args:
        profile_name: The profile name to be displayed in the chart title.
        traffic_data: A dictionary containing the traffic data (views and clones) for each date.
        theme_name: The theme name to be applied to the chart.
        bg_color: (Optional) A custom background color for the chart.

    Returns:
        A StreamingResponse containing the chart in SVG format.
    """
    # Load the theme
    theme = load_theme(theme_name)

    # Sort the dates
    sorted_dates = sorted(traffic_data.keys())
    # Extract the day part from the dates
    dates = [date.split('-')[-1] for date in sorted_dates]
    # Extract the number of clones
    clones = [traffic_data[date]["clones"] for date in sorted_dates]
    # Extract the number of views
    views = [traffic_data[date]["views"] for date in sorted_dates]
    # Get the background color, use the theme background color if not provided
    background_color = f"#{bg_color}" if bg_color else theme["background_color"]

    # Custom style
    custom_style = Style(
        background=background_color,
        plot_background=background_color,
        foreground=theme["text_color"],
        foreground_strong=theme["text_color"],
        foreground_subtle=theme["text_color"],
        guide_stroke_color=theme["grid_color"],
        major_guide_stroke_color=theme["grid_color"],
        opacity=0.6,
        opacity_hover=0.9,
        stroke_width=3,
        colors=(
            theme["line_colors"]["clones"],
            theme["line_colors"]["views"]
        )
    )

    # Create the line chart with curve interpolation
    line_chart = pygal.Line(
        style=custom_style,
        x_label_rotation=45,
        height=height,
        width=width,
        interpolate='hermite',
        legend_at_bottom=True,
        legend_box_size=6
    )

    # Set the title
    line_chart.title = f"{profile_name}'s Repo Traffic"
    # Set the x-axis title
    line_chart.x_title = "Days"
    # Set the y-axis title
    line_chart.y_title = "Traffic Count"
    line_chart.x_labels = dates
    line_chart.add('Clones', clones)
    line_chart.add('Views', views)

    # Render the SVG content
    svg_content = line_chart.render()

    return svg_content
