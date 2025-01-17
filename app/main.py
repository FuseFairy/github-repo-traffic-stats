from fastapi import FastAPI, Query, Response, HTTPException
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart

app = FastAPI()

# Create a TTL (time-to-live) cache with a max size of 1 and expiration time of 86400 seconds (24 hours)
cache = TTLCache(maxsize=1, ttl=86400)  # Cache for 24 hours

@app.get("/")
def root():
    return {"message": "Welcome to GitHub Traffic Stats API"}

@app.get("/api")
def get_traffic_chart(
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., 'rgba(0, 0, 0, 0)')")
):
    """
    Endpoint to get the traffic chart for a GitHub user's repository.
    It fetches traffic data from the GitHub API and generates a chart in SVG format.
    
    Args:
    - username: GitHub username whose traffic data is to be fetched.
    - theme: The theme to be applied to the chart.
    - bg_color: Optional background color for the chart.

    Returns:
    - A response containing the chart in SVG format.
    """
    try:
        # Check if traffic data for the user is cached
        if username in cache:
            traffic_data = cache[username]  # Retrieve from cache
        else:
            traffic_data = get_all_traffic_data(username)  # Fetch new traffic data from GitHub API
            cache[username] = traffic_data  # Store traffic data in cache

        profile_name = get_profile_name()  # Get the profile name
        chart_svg = generate_chart(profile_name, traffic_data, theme, bg_color)  # Generate the chart in SVG format

        return Response(content=chart_svg, media_type="image/svg+xml")  # Return the SVG chart as the response

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))  # Raise 404 if theme file is not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")  # Raise 500 for other errors
