from fastapi import FastAPI, Query, Response, HTTPException
from fastapi.responses import RedirectResponse
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI()

# Create a TTL (time-to-live) cache with a max size of 10 and expiration time of 86400 seconds (24 hours)
cache = TTLCache(maxsize=10, ttl=1800)

@app.get("/")
def root():
    return RedirectResponse(url="https://github.com/FuseFairy/github-repo-traffic")

@app.get("/api")
def get_traffic_chart(
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., '00000000' for transparent black, 'FFFFFF' for white without '#')"),
    clones_color: str = Query(None, description="Color for clones line (e.g., 'FF5733' for orange-red without '#')"),
    views_color: str = Query(None, description="Color for views line (e.g., '33FF57' for green without '#')"),
    height: int = Query(400, ge=400, description="Chart height in pixels"),
    width: int = Query(800, ge=800, description="Chart width in pixels"),
    exclude_repos: str = Query(None, description="Comma-separated list of repository names to exclude from the chart")
):
    """
    Endpoint to get the traffic chart for a GitHub user's repository.
    It fetches traffic data from the GitHub API and generates a chart in SVG format.
    
    Args:
        - username: GitHub username whose traffic data is to be fetched.
        - theme: The theme to be applied to the chart.
        - bg_color: Optional background color for the chart.
        - clones_color: Optional clones stroke color for the chart.
        - views_color: Optional views stroke color for the chart.
        - height: Height of the chart.
        - width: Width of the chart.
        - exclude_repos: Comma-separated list of repository names to exclude from the chart.

    Returns:
        A response containing the chart in SVG format.
    """
    try:
        # Check if traffic data is already cached for this username
        traffic_data_key = f"traffic_data_{username}"
        profile_name_key = f"profile_name_{username}"

        if traffic_data_key in cache and profile_name_key in cache:
            traffic_data = cache[traffic_data_key]
            profile_name = cache[profile_name_key]
        else:
            # Convert the comma-separated exclude_repos string into a list
            if exclude_repos:
                exclude_repos = exclude_repos.split(",")

            # Generate new traffic data and profile name
            traffic_data = get_all_traffic_data(username, exclude_repos)
            profile_name = get_profile_name()

            # Cache traffic data and profile name for 24 hours
            cache[traffic_data_key] = traffic_data
            cache[profile_name_key] = profile_name

        # Generate chart
        chart_svg = generate_chart(profile_name, traffic_data, theme, height, width, bg_color, clones_color, views_color)

        # Set appropriate Cache-Control headers for response caching
        headers = {
            "Cache-Control": "public, max-age=1800",  # Cache for 24 hours
            "Content-Disposition": "inline; filename=chart.svg"
        }
        
        # Create Response object and return it
        return Response(content=chart_svg, media_type="image/svg+xml", headers=headers)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))  # Raise 404 if theme file is not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")  # Raise 500 for other errors
